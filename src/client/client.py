import json
from panda3d.core import loadPrcFileData, WindowProperties
from ursina import *
from ursina.networking import *

from common.messages_from_server.message_types import MessageType
from client.ui.ui_manager import UIManager

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
def on_connect(connection, time_received):
    print(f"Connected to server at {connection.address}, time: {time_received}")
    UI_MANAGER.on_connected()
    # Handle post-connection setup

@rpc(peer)
def send_data(connection, time_received, message_type:str, msg:str):
    f = getattr(MessageType, message_type, None).value[0] #[0] since we have a singleton tuple
    if f:
        msg = json.loads(msg)
        f(msg, UI_MANAGER)
    else:
        raise ValueError(f"No function registered for message type: {message_type}")
    # Display message in chat UI

@rpc(peer)
def send_player(connection, time_received, player_info: str):
    print(f"Received player info from server: {player_info}")


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
        UI_MANAGER.input_handle(key)
    def update():
        peer.update()
        # Simple camera controls
        if held_keys['w']:
            camera.position += camera.forward * time.dt * 3
        if held_keys['s']:
            camera.position -= camera.forward * time.dt * 3
        if held_keys['a']:
            camera.position -= camera.right * time.dt * 3
        if held_keys['d']:
            camera.position += camera.right * time.dt * 3


    app.run()


if __name__ == '__main__':
    main()
