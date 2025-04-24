import os

from panda3d.core import loadPrcFileData, WindowProperties

# --- Panda3D Config ---
loadPrcFileData('', 'window-title Mindwar')
loadPrcFileData('', 'fullscreen 0')
loadPrcFileData('', 'undecorated 0')
loadPrcFileData('', 'win-size 1280 720')
loadPrcFileData('', 'win-origin 100 100')
loadPrcFileData('', 'show-frame-rate-meter 0')
loadPrcFileData('', 'window-type none')  # prevent premature window creation

# --- Start the game ---
from ursina import *
from game_manager import GameManager

def main():
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

    # Start the GameManager
    GameManager()

    app.run()

if __name__ == '__main__':
    main()

