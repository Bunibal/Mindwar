from logging import log
from ursina import *
from ursina import Vec3

from common.messages_from_server.message_types import MessageType
from server.game.game import Game
from entities.units.base_unit import UnitType, BaseUnitUI
from server.gamestate import GameState
from map import map_manager


class GameManager:
    def __init__(self, lobby_manager):
        self.games = {}
        self.lobbies = {}
        self.lobby_manager = lobby_manager

    def start_new_game(self, chosen_factions, lobby_id):
        new_game = Game(chosen_factions)
        self.games[new_game.uuid] = new_game
        self.lobbies[new_game.uuid] = lobby_id
        new_game.start_game()

        return new_game.uuid

    def end_turn(self, game_id):
        self.games[game_id].end_turn()

    def get_gamestate_serialized(self, game_id):
        game = self.games.get(game_id, None)
        if game:
            serialized_state = game.encode_game_state()
            return serialized_state