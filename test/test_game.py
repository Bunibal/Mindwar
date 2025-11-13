import json

from ursina import Ursina

from client.ui.ui_game_state import GameStateUI
from entities.factions.base_faction import FactionType
from map.map_manager import MapManagerUI
from server.game.game import Game
from server.lobby.lobby import LobbyPlayer

def test_game_initialization():
    player1 = LobbyPlayer("dummy_connection1")
    player2 = LobbyPlayer("dummy_connection2")
    factions = {
        player1.player_id: FactionType.HUMAN,
        player2.player_id: FactionType.HUMAN
    }
    game = Game(factions)
    assert game.current_player is None
    assert len(game.players) == 2
    game.start_game()
    print(game.encode_game_state())
    json.dumps(game.encode_game_state())

def test_gamestate_pass():
    
    player1 = LobbyPlayer("dummy_connection1")
    player2 = LobbyPlayer("dummy_connection2")
    factions = {
        player1.player_id: FactionType.HUMAN,
        player2.player_id: FactionType.HUMAN
    }
    app=Ursina()
    game = Game(factions)
    game.start_game()
    encoded_state  = game.encode_game_state()
    map_manager_ui = MapManagerUI()
    map_manager_ui.from_dict(encoded_state['map'])
    game_state_ui = GameStateUI(None)
    game_state_ui.load_game_state(encoded_state)


if __name__ == "__main__":
    test_game_initialization()
    test_gamestate_pass()
