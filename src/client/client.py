from panda3d.core import loadPrcFileData, WindowProperties
from ursina import *
from ursina.networking import *

from src.game_manager import GameManager
from src.client.ui.ui_manager import UIManager, input_handle

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

@rpc(peer)
def send_gamestate(connection, time_received, state: str):
    print(f"Received gamestate from server: {state}")
    # Update local gamestate accordingly

@rpc(peer)
def send_message(connection, time_received, player_id: int, message: str):
    print(f"Message from player {player_id}: {message}")
    # Display message in chat UI

@rpc(peer)
def do_action(connection, time_received, action: str, params: dict):
    print(f"Action from server: {action} with params {params}")
    # Execute action locally

@rpc(peer)
def send_lobby_list(connection, time_received, lobbies: list):
    print(f"Received lobby list from server: {lobbies}")
    # Update local lobby list UI


def main():
    global input, update
    app = Ursina(borderless=False)

    peer.start("localhost", 8080, is_host=False)
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

    ui_manager = UIManager(peer)
    ui_manager.start_menu()


    def input(key):
        if key == 's':
            peer.message(peer.get_connections()[0], "Hello, World!")
        #input_handle(key, ui_manager)

    def update():
        peer.update()

    app.run()


if __name__ == '__main__':
    main()
