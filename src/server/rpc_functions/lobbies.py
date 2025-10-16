LOBBY_FUNCTIONS_TO_REGISTER = []

def rpcreg(f):
    LOBBY_FUNCTIONS_TO_REGISTER.append(f)
    return f

@rpcreg
def get_lobby_list(connection, time_received):
    print(f"Player {connection.address} requested lobby list")
    # Send list of open lobbies
    # Hope that return works


@rpcreg
def create_lobby(connection, time_received, lobby_name: str, max_players: int):
    print(f"Player {connection.address} created lobby {lobby_name} with max players {max_players}")
    lobbies.append({'name': lobby_name, 'max_players': max_players, 'players': [connection.address]})
    # Create lobby
    # Add lobby to list/dict
    # Notify others

@rpcreg
def join_lobby(connection, time_received, lobby_id: int):
    print(f"Player {connection.address} joined lobby {lobby_id}")
    peer = connection.rpc_peer
    for c in peer.get_connections():
        peer.message(c, f"Joined lobby {lobby_id}")
    # Add player to lobby
    # Notify others in lobby
    # Send lobby info to player

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


@rpcreg
def press_start_button(connection, time_received):
    print(f"Player {connection.address} pressed start button")
    # Check if all players are ready
    # If yes, start game
    game.start_game()




