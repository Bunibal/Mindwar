from ursina import *

app = Ursina(title="Simple GLB Viewer")

# Simple lighting
DirectionalLight().look_at(Vec3(1, -1, -1))

# Ground reference
Entity(model='cube', color=color.gray, scale=(5, 0.1, 5), position=(0, -1, 0))

# Load the specific human infantry model
model_path = "assets/models/units/human/infantry.glb"

print(f"Trying to load: {model_path}")

try:
    # Load the model
    infantry_model = Entity(
        model=model_path,
        position=(0, 0, 0),
        scale=1,
        color=color.white
    )

    print("✅ Model loaded successfully!")
    print("   If you don't see it, try:")
    print("   - Mouse drag to look around")
    print("   - WASD to move camera")
    print("   - +/- to scale model")

except Exception as e:
    print(f"❌ Failed to load model: {e}")
    # Create a placeholder cube instead
    infantry_model = Entity(model='cube', color=color.red, scale=0.5)
    print("Created red cube as placeholder")

# Simple camera controls
camera.position = (0, 2, 5)
camera.look_at(Vec3(0, 0, 0))


def input(key):
    if key == '+' or key == '=':
        infantry_model.scale *= 1.2
        print(f"Scale: {infantry_model.scale}")
    elif key == '-':
        infantry_model.scale *= 0.8
        print(f"Scale: {infantry_model.scale}")
    elif key == 'r':
        infantry_model.rotation_y += 45
    elif key == 'q':
        quit()


def update():
    # Simple camera controls
    if held_keys['w']:
        camera.position += camera.forward * time.dt * 3
    if held_keys['s']:
        camera.position -= camera.forward * time.dt * 3
    if held_keys['a']:
        camera.position -= camera.right * time.dt * 3
    if held_keys['d']:
        camera.position += camera.right * time.dt * 3

    # Mouse look
    if held_keys['left mouse']:
        camera.rotation_y += mouse.velocity[0] * 50
        camera.rotation_x -= mouse.velocity[1] * 50


print("Controls:")
print("WASD - Move camera")
print("Mouse drag - Look around")
print("+/- - Scale model")
print("R - Rotate model")
print("Q - Quit")

app.run()