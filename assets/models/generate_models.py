# Re-run the previous hex generation after code execution state reset

import numpy as np
from pathlib import Path
from trimesh.creation import cylinder, cone
from trimesh import Trimesh, Scene

# Output directory
flat_top_dir = Path("/home/bunibal/PycharmProjects/Mindwar/assets/models/hex_tiles")
flat_top_dir.mkdir(parents=True, exist_ok=True)

def create_vertex_colored_mesh(mesh, color_rgb):
    rgba = np.array(color_rgb + (255,))
    mesh.visual.vertex_colors = np.tile(rgba, (len(mesh.vertices), 1))
    return mesh

def build_flat_top_hex(name, base_color, height=0.2, feature=None):
    side = 2.0
    top_z = height
    bottom_z = 0.0
    vertices = []
    faces = []

    # Flat-top orientation (angle shifted by 30 degrees)
    vertices.append([0, 0, bottom_z])
    for i in range(6):
        angle = np.pi / 6 + i * np.pi / 3
        x = side * np.cos(angle)
        y = side * np.sin(angle)
        vertices.append([x, y, bottom_z])

    vertices.append([0, 0, top_z])
    for i in range(6):
        angle = np.pi / 6 + i * np.pi / 3
        x = side * np.cos(angle)
        y = side * np.sin(angle)
        vertices.append([x, y, top_z])

    for i in range(1, 7):
        faces.append([0, i, 1 if i == 6 else i + 1])
    for i in range(7, 13):
        faces.append([7, i, 7 if i == 12 else i + 1])
    for i in range(1, 7):
        b1, b2 = i, 1 if i == 6 else i + 1
        t1, t2 = i + 6, 7 if i == 6 else i + 7
        faces.append([b1, b2, t1])
        faces.append([b2, t2, t1])

    base = Trimesh(vertices=vertices, faces=faces, process=False)
    base = create_vertex_colored_mesh(base, base_color)

    scene = Scene()
    scene.add_geometry(base, node_name='base')

    if feature == "tree":
        trunk = cylinder(radius=0.1, height=0.3)
        trunk.visual.vertex_colors = np.tile(np.array((139, 69, 19, 255)), (len(trunk.vertices), 1))
        trunk.apply_translation([0, 0, height])
        scene.add_geometry(trunk, node_name='trunk')

        leaves = cone(radius=0.4, height=0.6)
        leaves.visual.vertex_colors = np.tile(np.array((34, 139, 34, 255)), (len(leaves.vertices), 1))
        leaves.apply_translation([0, 0, height + 0.3])
        scene.add_geometry(leaves, node_name='leaves')

    elif feature == "mountain":
        peak = cone(radius=0.9, height=1.5, sections=6)
        peak.visual.vertex_colors = np.tile(np.array((128, 128, 128, 255)), (len(peak.vertices), 1))
        peak.apply_translation([0, 0, height])
        scene.add_geometry(peak, node_name='peak')

    scene.export(file_obj=flat_top_dir / f"{name}.glb", file_type='glb')

# Recreate the tiles
build_flat_top_hex("hex_grass", base_color=(128, 255, 128))
build_flat_top_hex("hex_water", base_color=(64, 164, 223))
build_flat_top_hex("hex_forest", base_color=(80, 200, 120), feature="tree")
build_flat_top_hex("hex_mountain", base_color=(100, 100, 100), feature="mountain")
build_flat_top_hex("hex_desert", base_color=(237, 201, 175))
build_flat_top_hex("hex_wetland", base_color=(106, 160, 115))
