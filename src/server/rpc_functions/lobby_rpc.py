import enum
import json

import ursina.networking

from common.messages_from_server.message_types import MessageType
from server.lobby import lobby

LOBBY_FUNCTIONS_TO_REGISTER = []

from server.handler import LOBBY_MANAGER


def rpcreg(f):
    LOBBY_FUNCTIONS_TO_REGISTER.append(f)
    return f


@rpcreg
def on_connect(connection, time_received):
    print(f"Player {connection.address} connected with name")
    player = LOBBY_MANAGER.connect_player(connection)
    connection.rpc_peer.send_player(connection, player.to_string())


@rpcreg
def on_disconnect(connection, time_received):
    print(f"Player {connection.address} disconnected")
    # player_id = connection.get_player_id()
    LOBBY_MANAGER.disconnect_player(connection)


@rpcreg
def set_player_name(connection, time_received, player_name: str):
    LOBBY_MANAGER.set_player_name(connection, player_name)


@rpcreg
def get_lobby_list(connection, time_received):
    print(f"Player {connection.address} requested lobby list")
    # lobbies = []
    # for lobby in LOBBY_MANAGER.lobbies.values():
    #     lobbies.append(str(lobby.to_dict()))
    send_data(connection, MessageType.LOBBY_LIST, LOBBY_MANAGER.lobbies)


@rpcreg
def create_lobby(connection, time_received, lobby_name: str, max_players: int):
    lobby_id = LOBBY_MANAGER.create_lobby(connection, lobby_name, max_players)
    send_data(connection, MessageType.LOBBY_INFO, lobby.to_json(LOBBY_MANAGER.lobbies[lobby_id]))


@rpcreg
def send_lobby_info(connection, time_received, lobby_id: str):
    lobby = LOBBY_MANAGER.get_lobby_info(connection, lobby_id)
    send_data(connection, MessageType.LOBBY_INFO, lobby)


def send_data(connection, message_type: MessageType, message, send_to_lobby=False):
    if send_to_lobby:
        # Get the player's lobby
        player = LOBBY_MANAGER._get_player_from_connection(connection)
        lobby = LOBBY_MANAGER._get_lobby_from_player(player)

        if lobby:
            # Send to all players in the same lobby
            for lobby_player in lobby.players:
                lobby_player.connection.rpc_peer.send_data(
                    lobby_player.connection,
                    message_type.name,
                    json.dumps(message, default=serialize)
                )
        else:
            # Player not in a lobby, send only to them
            connection.rpc_peer.send_data(connection, message_type.name, json.dumps(message, default=serialize))
    else:
        connection.rpc_peer.send_data(connection, message_type.name, json.dumps(message, default=serialize))


@rpcreg
def join_lobby(connection, time_received, lobby_id: str):
    print(f"Player {connection.address} joined lobby {lobby_id}")
    lobby = LOBBY_MANAGER.join_lobby(connection, lobby_id)
    send_data(connection, MessageType.LOBBY_INFO, lobby)


@rpcreg
def kick_player(connection, time_received, player_id: int):
    print(f"Player {connection.address} kicked player {player_id}")
    # Remove player from lobby
    # Notify others in lobby
    # check if player is host, and whether player_id is not host


@rpcreg
def leave_lobby(connection, time_received):
    print(f"Player {connection.address} left lobby")
    # Remove player from lobby
    # Notify others in lobby
    # If lobby empty, delete lobby


@rpcreg
def set_ready_status(connection, time_received, ready: bool):
    # 0 - not ready, 1 - ready, -1 - not interested in game
    print(f"Player {connection.address} set ready status to {ready}")
    # Update player status
    # Notify others
    # If all ready, start countdown


@rpcreg
def choose_faction(connection, time_received, faction: str):
    print(f"Player {connection.address} chose faction {faction}")
    # Update player faction
    # Notify others in lobby


# @rpcreg
# def press_start_button(connection, time_received):
#     print(f"Player {connection.address} pressed start button")
#     # Check if all players are ready
#     # If yes, start game
#     game.start_game()


def serialize(obj):
    # If the object is a basic type, return as is
    if isinstance(obj, ursina.networking.Connection):
        return None
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    # If the object is a list or tuple, serialize each item recursively
    elif isinstance(obj, (list, tuple)):
        return [serialize(item) for item in obj]
    # If the object is a dictionary, serialize keys and values recursively
    elif isinstance(obj, dict):
        return {serialize(key): serialize(value) for key, value in obj.items()}
    # For any other object, try to serialize its __dict__ recursively
    elif isinstance(obj, enum.Enum):
        return obj.name
    elif hasattr(obj, '__dict__'):
        return {key: serialize(value) for key, value in obj.__dict__.items()}
    else:
        # Fallback to string representation if type is not serializable
        return str(obj)
