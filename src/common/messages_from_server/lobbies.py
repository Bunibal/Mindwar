def lobby_info_received(message: str, ui_manager):
    print(f"Received lobby info: {message}")
    ui_manager.lobby_info_received(message)
