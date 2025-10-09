from src.entities.units.base_unit_logic import UnitType, BaseUnit
from src.gamestate import GameState
from src.map import map_manager_logic


class Game:
    def __init__(self):
        self.current_player = None
        self.chosen_factions = None
        self.map_manager = None
        self.gamestate = GameState()
        self.gamestate.game_manager = self

    def setup_game(self):
        self.gamestate.game_state = "game"
        self.gamestate.game_map = []

    def start_game(self):
        self.prepare_game()
        self.current_player = self.chosen_factions[0]

    def prepare_game(self):
        self.load_start_units()

    def load_start_units(self):
        for player in self.chosen_factions:
            start_config = player.units_start_config
            for config in start_config:
                if config["all_fields"] is True:
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in self.map_manager.action_fields:
                                unit = BaseUnit(player.name, unit_type, grid_position=action_field.grid_position,
                                                position=action_field.position + (0, 0, -1),
                                                )  # parent=player
                                player.units.append(unit)
                else:
                    randomized_fields = self.map_manager.get_random_action_fields(config["n_selected_fields"])
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in randomized_fields:
                                unit = BaseUnit(player.name, unit_type, action_field.grid_position,
                                                action_field.position,
                                                parent=player)
                                player.units.append(unit)

    def end_turn(self):
        self.current_player = self.chosen_factions[
            (self.chosen_factions.index(self.current_player) + 1) % len(self.chosen_factions)]

    def generate_random_map(self, rows=10, cols=20, n_action_fields=10, n_streets=20, weights=None):
        if self.map_manager:
            self.destroy_map()
        self.map_manager = map_manager_logic.MapManager(
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
