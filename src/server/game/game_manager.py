from logging import log
from ursina import *
from ursina import Vec3

from common.messages_from_server.message_types import MessageType
from server.game.game import Game
from entities.units.base_unit import UnitType, BaseUnitUI
from server.gamestate import GameState
from map import map_manager
from utils.logger import logger


class GameManager:
    def __init__(self, lobby_manager):
        self.games = {}
        self.lobbies = {}
        self.lobby_manager = lobby_manager
        self.connections_to_games = {}

    def start_new_game(self, chosen_factions, connections, lobby_id):
        new_game = Game(chosen_factions)
        self.games[new_game.uuid] = new_game
        self.lobbies[new_game.uuid] = lobby_id
        for connection in connections.values():
            self.connections_to_games[connection] = new_game.uuid
        new_game.start_game()

        return new_game.uuid

    def end_turn(self, connection):
        game_id = self.connections_to_games.get(connection, None)
        if game_id:
            self.games[game_id].end_turn()
            return 

    def ga_move_unit(self, connection, unit_id_str:str, new_grid_position):
        game_id = self.connections_to_games.get(connection, None)
        if game_id:
            game = self.games.get(game_id, None)
            if game:
                game.ga_move_unit(unit_id_str, new_grid_position)
                return game.pop_event_queue()
            else:
                logger.error(f"Game with id '{game_id}' not found for connection {connection}.")
        else:
            logger.warning(f"No game found for connection {connection}.")

        

    def get_gamestate_serialized(self, game_id):
        game = self.games.get(game_id, None)
        if game:
            serialized_state = game.encode_game_state()
            return serialized_state