
from ursina import *

app = Ursina()

models = {
    'straight': 'assets/models/hex_streets/street_straight.glb',
    'curve_small': 'assets/models/hex_streets/street_curve_small.glb',
    'curve_large': 'assets/models/hex_streets/street_curve_large.glb'
}

angle_steps = [0, 60, 120, 180, 240, 300]
spacing_x = 4
spacing_y = 4

for row_index, (label, model_path) in enumerate(models.items()):
    for col_index, rot in enumerate(angle_steps):
        x = col_index * spacing_x
        y = -row_index * spacing_y

        road = Entity(
            model=model_path,
            position=(x, y, 0),
            rotation_z=rot,
            scale=0.5,
            color=color.white
        )

        label_text = Text(
            text=f'{label}\n{rot}°',
            world_parent=road,
            position = (0, 0.5, 0),
            scale=10,
            origin=(0, 0),
            color=color.azure
        )

camera.z = -30
EditorCamera()
app.run()
