from common.messages_from_server.message_types import MessageType
from server.handler import GAME_MANAGER, LOBBY_MANAGER
from server.rpc_functions.lobby_rpc import send_data


GAMEACTIONS_FUNCTIONS_TO_REGISTER = []

def rpcreg(f):
    GAMEACTIONS_FUNCTIONS_TO_REGISTER.append(f)
    return f

@rpcreg
def end_turn(connection, time_received):
    print(f"Player {connection.address} ended their turn")
    game.end_turn()
    # Notify others about new current player


@rpcreg
def move_unit(connection, time_received, unit_id: int, new_grid_position: tuple[int, int]):
    print(f"Player {connection.address} requests to move unit {unit_id} to {new_grid_position}")
    events = GAME_MANAGER.ga_move_unit(connection, unit_id, new_grid_position)
    if events:
        send_data(connection, MessageType.GAME_EVENTS, events, send_to_lobby=True)


# ..... more game actions .....