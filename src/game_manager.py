from ursina import *
from ursina import Vec3

from server.game import Game
from entities.units.base_unit import UnitType, BaseUnitUI
from server.gamestate import GameState
from map import map_manager
from client.ui.ui_manager import UIManager


class GameManager:
    def __init__(self):
        self.game = Game()
        self.ui_manager = UIManager(self)
        self.ui_manager.start_menu()

    def setup_game_locally(self):
        self.game.setup_game()
        self.ui_manager.setup_game_ui()

    def start_game_locally(self):
        self.game.start_game()
        self.ui_manager.game_ui()

        for player in self.chosen_factions:
            start_config = player.units_start_config
            for config in start_config:
                if config["all_fields"] is True:
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in self.map_manager.action_fields:
                                unit = BaseUnitUI(player.name, unit_type, grid_position=action_field.grid_position,
                                                position=action_field.position + (0, 0, -1),
                                                )  # parent=player
                                player.units.append(unit)
                else:
                    randomized_fields = self.map_manager.get_random_action_fields(config["n_selected_fields"])
                    for unit_type in UnitType:
                        for i in range(config[unit_type.name]):
                            for action_field in randomized_fields:
                                unit = BaseUnitUI(player.name, unit_type, action_field.grid_position,
                                                action_field.position,
                                                parent=player)
                                player.units.append(unit)

    def end_turn(self):
        self.game.end_turn()

    def destroy_map(self):
        for tile in self.gamestate.game_map:
            destroy(tile)
        del self.map_manager
        self.map_manager = None
        self.gamestate.game_map = []
        scene.clear()
