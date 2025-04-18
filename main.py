from panda3d.core import loadPrcFileData, WindowProperties
import os

# --- Set Panda3D window config BEFORE importing Ursina ---
loadPrcFileData('', 'window-title Mindwar')
loadPrcFileData('', 'fullscreen 0')
loadPrcFileData('', 'undecorated 0')
loadPrcFileData('', 'win-size 1280 720')
loadPrcFileData('', 'win-origin 100 100')
loadPrcFileData('', 'show-frame-rate-meter 0')
loadPrcFileData('', 'window-type none')  # prevent premature window creation

# --- Import Ursina and your game components ---
from ursina import *
from map.map_manager import MapManager


from ursina import camera, Vec3
from tiles.base_tile import BaseTile
def center_camera(rows, cols):
    # Get the world position of the center tile
    x, y, z = BaseTile.hex_to_world(rows / 2, cols / 2)

    # Enable perspective projection
    camera.orthographic = False
    camera.fov = 50

    # Position the camera behind and above the center tile
    camera.position = (x, y - 85, -50)

    # Make the camera look at the center tile
    camera.look_at(Vec3(x, y, 0))



def main():
    app = Ursina(borderless=False)
    window.exit_button.visible = False  # Hide extra exit button

    # Create window properties
    props = WindowProperties()
    props.setTitle('Mindwar')
    props.setUndecorated(False)
    props.setOrigin(100, 100)
    props.setSize(1280, 720)
    props.setFullscreen(False)

    # Set icon using absolute path for better compatibility
    icon_path = os.path.abspath('/home/bunibal/PycharmProjects/Mindwar/assets/ui/mindwar_icon.ico')
    if os.path.exists(icon_path):
        props.setIconFilename(icon_path)
    else:
        print(f"⚠️ Icon not found at: {icon_path}")

    # Apply window settings to Panda3D base window
    from ursina import application
    application.base.win.requestProperties(props)

    # Generate game content
    map_manager = MapManager(rows=10, cols=20)
    map_manager.generate_map()

    # Lighting
    sun = DirectionalLight()
    sun.look_at(Vec3(1, -1, -1))
    AmbientLight(color=color.rgba(120, 120, 120, 0.5))

    # Camera
    center_camera(10, 20)

    # Run app
    app.run()


if __name__ == '__main__':
    main()
