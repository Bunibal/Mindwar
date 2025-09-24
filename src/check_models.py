from ursina import *

from src import settings

app = Ursina()

models = [file for file in os.listdir(settings.HEX_STREETS_DIR) if file.endswith('.glb') or file.endswith('.gltf')]

index = 0
tile = None
info_text = None

# Persistent reference grid + cube
Entity(model='plane', scale=100, color=color.gray, y=-1)
Entity(model='cube', color=color.red, scale=0.2, position=(0, 0, 0))


def load_model_by_index(i):
    global tile, info_text
    if tile:
        destroy(tile)
    if info_text:
        destroy(info_text)

    model_path = settings.HEX_STREETS_DIR + models[i]
    print(f"\n--- Loading: {model_path} ---")

    tile = Entity(model=model_path, position=(0, 0, 0), unlit=True)

    # Debug info
    print("Entity created.")
    print("Model:", tile.model)
    print("Bounds center:", tile.bounds.center)
    print("Bounds size:", tile.bounds.size)
    print("Scale before:", tile.scale)

    # Normalize size if needed
    max_dim = max(tile.bounds.size)
    if max_dim > 0:
        tile.scale = 3 / max_dim
        print("Scale adjusted to:", tile.scale)

    info_text = Text(models[i], position=(-0.5, 0.4), scale=2)


def input(key):
    global index
    if key == 'right arrow':
        index = (index + 1) % len(models)
        load_model_by_index(index)
    elif key == 'left arrow':
        index = (index - 1) % len(models)
        load_model_by_index(index)


# Lighting
DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgb(150, 150, 150))

# Camera stays still
camera.position = (0, 5, -10)
camera.rotation_x = 30

load_model_by_index(index)
EditorCamera()  # ← this stays active the whole time

app.run()
