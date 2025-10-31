import uuid
from entities.factions.base_faction import BaseFaction, FactionType
from entities.units.base_unit_logic import UnitType, BaseUnitLogic
from server.gamestate import GameState
from map.map_manager_logic import MapManagerLogic


class Game:
    def __init__(self, factions:dict):
        self.current_player = None
        self.players  = list(factions.keys()) # Player IDs
        self.factions = {pid:BaseFaction("TBD", ftype) for pid, ftype in factions.items()}
        self.uuid = uuid.uuid4()
        self.gamestate = GameState()


    def start_game(self):
        self.game_state = "game"
        self.game_map = []
        self.prepare_game()
        self.current_player = 0
        self.generate_random_map()

    def prepare_game(self):
        self.load_start_units()

    def load_start_units(self):
        for player, faction in self.factions.items():
            start_config = player.units_start_config
            for config in start_config:
                if config["all_fields"] is True:
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in self.map_manager.action_fields:
                                unit = BaseUnitLogic(player.name, unit_type, grid_position=action_field.grid_position
                                                )  # parent=player
                                player.units.append(unit)
                else:
                    randomized_fields = self.map_manager.get_random_action_fields(config["n_selected_fields"])
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in randomized_fields:
                                unit = BaseUnitLogic(player.name, unit_type, action_field.grid_position)
                                player.units.append(unit)

    def end_turn(self):
        self.current_player  = (self.current_player + 1) % len(self.players)

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


    def encode_game_state(self):
        state = {
            "current_player": self.current_player.name if self.current_player else None,
            "chosen_factions": [player.name for player in self.chosen_factions] if self.chosen_factions else [],
            "map": [tile.to_string() for tile in self.game_map] if self.game_map else [],
            "game_state": self.game_state,
        }
        return state

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
