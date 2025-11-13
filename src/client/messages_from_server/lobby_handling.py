def lobby_info_received(message: str, ui_manager):
    print(f"Received lobby info: {message}")
    ui_manager.lobby_info_received(message)


def send_lobby_list(lobbies: list[str], ui_manager):
    """Send the list of lobbies from server to client. (Meaning the client will be receiving)"""
    print(f"Received lobby list from server: {lobbies}")

    ui_manager.lobby_list_received(lobbies)
    # Update local lobby list UIˆ

def game_started(game_state: str, ui_manager):
    print("Game has started!")
    ui_manager.game_started(game_state)
