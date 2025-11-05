from entities.factions.base_faction import FactionType
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
    print(game.game_map)
    print("--------------------")
    for pid, faction in game.factions.items():
        print(f"Player ID: {pid}, Faction: {faction}")
        print(f"Units: {faction.units}")
    
if __name__ == "__main__":
    test_game_initialization()
