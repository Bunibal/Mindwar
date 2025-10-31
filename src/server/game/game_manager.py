from ursina import *
from ursina import Vec3

from server.game.game import Game
from entities.units.base_unit import UnitType, BaseUnitUI
from server.gamestate import GameState
from map import map_manager


class GameManager:
    def __init__(self):
        self.games = {}

    def start_new_game(self, chosen_factions):
        new_game = Game(chosen_factions)
        self.games[new_game.uuid] = new_game
        new_game.start_game()
        return

        for player in chosen_factions:
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

    def end_turn(self, game_id):
        self.games[game_id].end_turn()

