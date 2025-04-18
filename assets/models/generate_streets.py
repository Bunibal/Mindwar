# Re-run street model generation after code state reset

import numpy as np
from trimesh import Trimesh, Scene
from trimesh.creation import box
from pathlib import Path

street_dir = Path("/home/bunibal/PycharmProjects/Mindwar/assets/models/hex_streets")
street_dir.mkdir(parents=True, exist_ok=True)

from trimesh.transformations import rotation_matrix

def create_angled_street_fixed(name="street_edge_corner", angle_deg=60, arm_length=1.7, width=0.4, height=0.05):
    scene = Scene()
    color = np.array([139, 69, 19, 255])

    # Arm 1 (horizontal)
    box1 = box(extents=(arm_length, width, height))
    box1.apply_translation([arm_length / 2, 0, 0])

    # Arm 2 (rotated)
    box2 = box(extents=(arm_length, width, height))
    box2.apply_translation([arm_length / 2, 0, 0])

    # Rotation for arm 2
    angle_rad = np.radians(angle_deg)
    R = rotation_matrix(angle_rad, [0, 0, 1])  # Rotate around Z axis
    box2.apply_transform(R)

    # Apply vertex colors
    box1.visual.vertex_colors = np.tile(color, (len(box1.vertices), 1))
    box2.visual.vertex_colors = np.tile(color, (len(box2.vertices), 1))

    scene.add_geometry(box1, node_name="arm1")
    scene.add_geometry(box2, node_name="arm2")
    scene.export(file_obj=street_dir / f"{name}.glb", file_type="glb")

# Re-run fixed version

create_angled_street_fixed(name="street_curve_large", angle_deg=120)
create_angled_street_fixed(name="street_curve_small", angle_deg=60)
create_angled_street_fixed(name="street_straight", angle_deg=180)



