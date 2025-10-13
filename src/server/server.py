from panda3d.core import loadPrcFileData

from ursina import *
from ursina.networking import *

from src.server.game import Game
from src.server.lobbies import Lobbies

import time

#app = Ursina(borderless=False)
peer = RPCPeer()
game = Game()

lobby = Lobbies(peer)
@rpc(peer)
def on_connect(connection, time_received):
    print(f"New connection from {connection.address}")
    # Register Player and assign some UUID
    # Map UUID to IP address somehow
    # Notify others about new player
    # Check if disconnected before (if game running)
    # Send open lobbies

@rpc(peer)
def on_disconnect(connection, time_received):
    print(f"Connection lost from {connection.address}")
    # Notify others
    # Maybe pause? Remember ip address?

@rpc(peer)
def ragequit(connection, time_received, message: str):
    lobby.ragequit(connection, time_received, message)
    print(f"Player {connection.address} ragequit")
    # Notify others
    # Maybe pause? Remember ip address?
    # Have an LLM check whether the reason is legimate

@rpc(peer)
def get_lobby_list(connection, time_received):
    print(f"Player {connection.address} requested lobby list")
    # Send list of open lobbies
    # Hope that return works

for f in [create_lobby, join_lobby, kick_player, leave_lobby, set_ready_status, choose_faction, press_start_button,
          message, end_turn, move_unit]:
    peer.register_procedure(f)

@rpc(peer)
def create_lobby(connection, time_received, lobby_name: str, max_players: int):
    print(f"Player {connection.address} created lobby {lobby_name} with max players {max_players}")
    # Create lobby
    # Add lobby to list/dict
    # Notify others

@rpc(peer)
def join_lobby(connection, time_received, lobby_id: int):
    print(f"Player {connection.address} joined lobby {lobby_id}")
    # Add player to lobby
    # Notify others in lobby
    # Send lobby info to player

@rpc(peer)
def kick_player(connection, time_received, player_id: int):
    print(f"Player {connection.address} kicked player {player_id}")
    # Remove player from lobby
    # Notify others in lobby
    # check if player is host, and whether player_id is not host

@rpc(peer)
def leave_lobby(connection, time_received):
    print(f"Player {connection.address} left lobby")
    # Remove player from lobby
    # Notify others in lobby
    # If lobby empty, delete lobby

@rpc(peer)
def set_ready_status(connection, time_received, ready: bool):
    # 0 - not ready, 1 - ready, -1 - not interested in game
    print(f"Player {connection.address} set ready status to {ready}")
    # Update player status
    # Notify others
    # If all ready, start countdown


@rpc(peer)
def choose_faction(connection, time_received, faction: str):
    print(f"Player {connection.address} chose faction {faction}")
    # Update player faction
    # Notify others in lobby


@rpc(peer)
def press_start_button(connection, time_received):
    print(f"Player {connection.address} pressed start button")
    # Check if all players are ready
    # If yes, start game
    game.start_game()


@rpc(peer)
def message(connection, time_received, msg: str):
    print(msg)
    # Send message to all other players

@rpc(peer)
def end_turn(connection, time_received):
    print(f"Player {connection.address} ended their turn")
    game.end_turn()
    # Notify others about new current player

@rpc(peer)

@rpc(peer)
def move_unit(connection, time_received, unit_id: int, new_grid_position: tuple):
    print(f"Player {connection.address} moved unit {unit_id} to {new_grid_position}")
    # Find unit by id
    # Check if move is valid
    # Update unit position
    # Notify others

# ..... more game actions .....

peer.start("localhost", 8080, is_host=True)

if __name__ == '__main__':
    while True:
        peer.update()
        time.sleep(0.01)
#app.run()
 