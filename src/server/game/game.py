import uuid
from entities.factions.base_faction import BaseFaction, FactionType
from entities.units.base_unit_logic import UnitType, BaseUnitLogic
from common.messages_from_server.game_events import GameEventType
from server.gamestate import GameState
from map.map_manager_logic import MapManagerLogic
from utils.logger import logger

class Game:
    def __init__(self, factions:dict):
        """factions: dict[player_id: uuid, faction_type: FactionType]"""
        self.current_player = None
        self.players  = list(factions.keys()) # Player IDs
        self.factions = {pid:BaseFaction("TBD", ftype) for pid, ftype in factions.items()}
        self.uuid = uuid.uuid4()
        self.gamestate = GameState()
        self.map_manager = None
        self.event_queue = []


    def start_game(self):
        self.game_state = "game"
        self.game_map = []
        self.prepare_game()
        self.current_player = 0
        

    def prepare_game(self):
        self.generate_random_map()
        self.load_start_units()

    def load_start_units(self):
        for player_id, faction in self.factions.items():
            start_config = faction.units_start_config
            for config in start_config:
                if config["all_fields"] is True:
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in self.map_manager.action_fields:
                                unit = BaseUnitLogic(faction.faction_type, unit_type, grid_position=action_field.grid_position
                                                )  # parent=player
                                self.add_unit(player_id, unit)
                else:
                    randomized_fields = self.map_manager.get_random_action_fields(config["n_selected_fields"])
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in randomized_fields:
                                unit = BaseUnitLogic(player.name, unit_type, action_field.grid_position)
                                player.units.append(unit)

    def end_turn(self):
        self.current_player  = (self.current_player + 1) % len(self.players)

    def add_unit(self, player_id, unit):
        self.factions[player_id].units.append(unit)

    def generate_random_map(self, rows=10, cols=20, n_action_fields=10, n_streets=20, weights=None):
        if self.map_manager:
            self.destroy_map()
        self.map_manager = MapManagerLogic(
            rows=rows,
            cols=cols,
            n_action_fields=n_action_fields,
            n_streets=n_streets,
            terrain_weights=weights)
        self.game_map = self.map_manager.generate_map()
        self.gamestate.game_map = self.game_map
        # sun = DirectionalLight()
        # sun.look_at(Vec3(1, -1, -1))
        # AmbientLight(color=color.rgba(120, 120, 120, 0.5))
        self.gamestate.game_state = "game"

    def destroy_map(self):
        del self.map_manager
        self.map_manager = None
        self.gamestate.game_map = []

    @property
    def units(self):
        all_units = []
        for faction in self.factions.values():
            all_units.extend(faction.units)
        return all_units

    def encode_game_state(self):
        units_serialized = [self.serialize_unit(unit) for unit in self.units]
        state = {
            "current_player": self.current_player,
            "units": units_serialized,
            "factions": {pid: faction.faction_type.name for pid, faction in self.factions.items()},
            "map": self.map_manager.to_dict(),
            "game_state": self.game_state,
        }
        return state
    
    def serialize_unit(self, unit: BaseUnitLogic):
        return {
            "unit_id": unit.unit_id,
            "faction": unit.faction,
            "unit_type": unit.type.name,
            "grid_position": unit.grid_position
        }
    
    def _get_unit_by_id(self, unit_id):
        if isinstance(unit_id, str):
            unit_id = uuid.UUID(unit_id)
        for unit in self.units:
            if unit.unit_id == unit_id:
                return unit
        return None
    
    def ga_move_unit(self, unit_id_str, new_grid_position):
        # Find the unit by its ID
        unit = self._get_unit_by_id(unit_id_str)
        if unit:
            self.event_move_unit(unit, new_grid_position)
            return True
        else:
            logger.error(f"Unit with id '{unit_id_str}' not found.")

    def event_move_unit(self, unit, new_grid_position):
        unit.grid_position = new_grid_position
        self.event_queue.append({
            "event_type": GameEventType.MOVE_UNIT,
            "unit_id": unit.unit_id,
            "new_grid_position": new_grid_position
        })

    def pop_event_queue(self):
        events = tuple(self.event_queue)
        self.event_queue.clear()
        return events


    def build_action(self):
        pass

    def recruit_action(self):
        pass

    def fight_action(self):
        pass

    def move_action(self):
        pass

    def gather_action(self):
        pass
