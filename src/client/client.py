from panda3d.core import loadPrcFileData, WindowProperties
from ursina import *
from ursina.networking import *

from client.messages_from_server.message_types import MessageType
from src.client.ui.ui_manager import UIManager

# --- Panda3D Config ---
loadPrcFileData('', 'window-title Mindwar')
loadPrcFileData('', 'fullscreen 0')
loadPrcFileData('', 'undecorated 0')
loadPrcFileData('', 'win-size 1280 720')
loadPrcFileData('', 'win-origin 100 100')
loadPrcFileData('', 'show-frame-rate-meter 0')
loadPrcFileData('', 'window-type none')  # prevent premature window creation


# --- Start the game ---

peer = RPCPeer()
UI_MANAGER = UIManager(peer)

@rpc(peer)
def send_gamestate(connection, time_received, state: str):
    print(f"Received gamestate from server: {state}")
    # Update local gamestate accordingly

@rpc(peer)
def on_connect(connection, time_received):
    print(f"Connected to server at {connection.address}, time: {time_received}")
    UI_MANAGER.on_connected()
    # Handle post-connection setup

@rpc(peer)
def send_message(connection, time_received, player_id: int, message: str):
    print(f"Message from player {player_id}: {message}")
    # Display message in chat UI

@rpc(peer)
def send_data(connection, time_received, message_type:str, msg: str):
    f = getattr(MessageType, message_type, None)
    if f:
        f(msg, UI_MANAGER)
    else:
        raise ValueError(f"No function registered for message type: {message_type}")
    # Display message in chat UI

@rpc(peer)
def send_player(connection, time_received, player_info: str):
    print(f"Received player info from server: {player_info}")
    # Update local player info
# @rpc(peer)
# def send_anything(connection, time_received, msg_type:str, data: str):
#     execute(connection, time_received, msg_type, data, UI_MANAGER)
#     print(f"Received data from server: {data}")
    # Process received data
@rpc(peer)
def do_action(connection, time_received, action: str, params: dict):
    print(f"Action from server: {action} with params {params}")
    # Execute action locally



@rpc(peer)
def send_lobby_list(connection, time_received, lobbies: list[str]):
    """Send the list of lobbies from server to client. (Meaning the client will be receiving)"""
    print(f"Received lobby list from server: {lobbies}")
    UI_MANAGER.lobby_list_received(lobbies)
    # Update local lobby list UI

@rpc(peer)
def send_lobby_info(connection, time_received, lobby_info: str):
    print(f"Received lobby info from server: {lobby_info}")
    UI_MANAGER.lobby_info_received(lobby_info)
    # Update local lobby info UI

def main():
    global input, update
    app = Ursina(borderless=False)

    window.exit_button.visible = False

    props = WindowProperties()
    props.setTitle('Mindwar')
    props.setUndecorated(False)
    props.setOrigin(100, 100)
    props.setSize(1280, 720)
    props.setFullscreen(False)
    print(os.getcwd())

    icon_path = os.path.abspath('../assets/ui/mindwar_icon.ico')
    if os.path.exists(icon_path):
        props.setIconFilename(icon_path)
    else:
        print(f"⚠️ Icon not found at: {icon_path}")

    from ursina import application
    application.base.win.requestProperties(props)

    
    UI_MANAGER.start_menu()


    def input(key):
        if key == 's':
            peer.message(peer.get_connections()[0], "Hello, World!")
        if key == 'l':
            peer.create_lobby(peer.get_connections()[0], "Test Lobby", 4)
        if key == "r":
            peer.get_lobby_list(peer.get_connections()[0])
        #input_handle(key, ui_manager)

    def update():
        peer.update()


    app.run()


if __name__ == '__main__':
    main()
