# Re-run street model generation after code state reset

import numpy as np
from trimesh import Trimesh, Scene
from trimesh.creation import box
from pathlib import Path

street_dir = Path("/home/bunibal/PycharmProjects/Mindwar/assets/models/hex_streets")
street_dir.mkdir(parents=True, exist_ok=True)

def generate_street_mesh(name, shape='straight'):
    scene = Scene()
    color_gray = np.array([150, 150, 150, 255])

    if shape == 'straight':
        street = box(extents=(1.8, 0.4, 0.05))  # long and thin
    elif shape == 'curve_small':
        arc = []
        steps = 8
        radius = 0.7
        width = 0.3
        for i in range(steps):
            angle = np.pi / 2 * i / (steps - 1)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            arc.append([x, y])
        arc = np.array(arc)
        arc_path = []
        for offset in [-width/2, width/2]:
            arc_path.append(np.column_stack([arc[:,0] + offset*np.sin(np.linspace(0, np.pi/2, steps)),
                                             arc[:,1] - offset*np.cos(np.linspace(0, np.pi/2, steps))]))
        vertices = np.concatenate(arc_path)
        z_low = np.zeros((len(vertices)//2, 1))
        z_high = np.full((len(vertices)//2, 1), 0.05)
        verts = np.concatenate([np.column_stack([vertices[:len(vertices)//2], z_low]),
                                np.column_stack([vertices[len(vertices)//2:], z_high])])
        faces = [[i, i+1, i+2] for i in range(len(verts)-2)]
        street = Trimesh(vertices=verts, faces=faces, process=False)

    elif shape == 'curve_large':
        arc = []
        steps = 8
        radius = 1.2
        width = 0.4
        for i in range(steps):
            angle = np.pi / 2 * i / (steps - 1)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            arc.append([x, y])
        arc = np.array(arc)
        arc_path = []
        for offset in [-width/2, width/2]:
            arc_path.append(np.column_stack([arc[:,0] + offset*np.sin(np.linspace(0, np.pi/2, steps)),
                                             arc[:,1] - offset*np.cos(np.linspace(0, np.pi/2, steps))]))
        vertices = np.concatenate(arc_path)
        z_low = np.zeros((len(vertices)//2, 1))
        z_high = np.full((len(vertices)//2, 1), 0.05)
        verts = np.concatenate([np.column_stack([vertices[:len(vertices)//2], z_low]),
                                np.column_stack([vertices[len(vertices)//2:], z_high])])
        faces = [[i, i+1, i+2] for i in range(len(verts)-2)]
        street = Trimesh(vertices=verts, faces=faces, process=False)

    street.visual.vertex_colors = np.tile(color_gray, (len(street.vertices), 1))
    scene.add_geometry(street)
    scene.export(file_obj=street_dir / f"{name}.glb", file_type='glb')

# Generate the three road types
generate_street_mesh("street_straight", shape='straight')
generate_street_mesh("street_curve_small", shape='curve_small')
generate_street_mesh("street_curve_large", shape='curve_large')

