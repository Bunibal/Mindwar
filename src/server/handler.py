from server.game.game_manager import GameManager
from server.lobby.lobby_manager import LobbyManager


LOBBY_MANAGER = LobbyManager()
GAME_MANAGER = GameManager(LOBBY_MANAGER)