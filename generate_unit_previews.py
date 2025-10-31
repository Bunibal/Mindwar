from ursina import *
import os
from panda3d.core import Texture, FrameBufferProperties, WindowProperties, GraphicsOutput, GraphicsPipe, PNMImage

# Replace these with your actual imports
from entities.units.base_unit import BaseUnitUI
from entities.factions.base_faction import FactionType
from entities.factions.base_faction import UnitType

app = Ursina(borderless=True)

# Ensure output directory exists
output_dir = 'assets/models/'
os.makedirs(output_dir, exist_ok=True)

# Settings
render_size = (256, 256)
unit_scale = 1.0
render_delay = 1 / 30  # Wait time to ensure the render finishes

# All unit-faction combinations
unit_faction_pairs = [(unit_type, faction) for unit_type in UnitType for faction in FactionType]
current_index = 0

# Prepare a preview scene
preview_root = NodePath('preview_root')

# Setup Panda3D render buffer
win_props = WindowProperties.size(*render_size)
fb_props = FrameBufferProperties()
fb_props.set_rgb_color(True)
fb_props.set_alpha_bits(1)
fb_props.set_depth_bits(1)

preview_buffer = base.graphicsEngine.make_output(
    base.pipe,
    "Preview Buffer",
    -2,
    fb_props,
    win_props,
    GraphicsPipe.BFRefuseWindow,
    base.win.get_gsg(),
    base.win
)

preview_texture = Texture()
preview_buffer.add_render_texture(preview_texture, GraphicsOutput.RTMCopyRam)

# Create a preview camera
preview_camera_np = base.makeCamera(preview_buffer)
preview_camera_np.reparent_to(preview_root)
preview_camera_np.set_pos(0, 0, 0)
preview_camera_np.look_at(0, 0, 4)

# Add lighting to the preview scene
from panda3d.core import DirectionalLight as PandaDirectionalLight

# Add lighting to the preview scene
panda_light = PandaDirectionalLight("preview_light")
light_np = preview_root.attach_new_node(panda_light)
light_np.set_pos(2, -2, 5)
preview_root.set_light(light_np)

# Preview model holder
model_entity = None

def setup_render_pair(unit_type, faction):
    global model_entity
    if model_entity:
        model_entity.remove_node()

    model_entity = BaseUnitUI(
        unit_type=unit_type,
        faction=faction.name,
        parent=scene,
        position=(0, 0, 4),
        scale=unit_scale,
        rotation_y=180
    )
    model_entity.reparent_to(preview_root)

def save_current_preview(unit_type, faction):
    filename = f"{unit_type.name.lower()}_{faction.name.lower()}.png"
    path = os.path.join(output_dir, filename)

    # Convert texture to image
    pnm_image = PNMImage()
    preview_texture.store(pnm_image)
    pnm_image.write(path)

    print(f"✅ Saved: {filename}")

def render_next():
    global current_index

    if current_index >= len(unit_faction_pairs):
        print("🎉 All previews generated.")
        application.quit()
        return

    unit_type, faction = unit_faction_pairs[current_index]
    print(f"🔄 Rendering: {unit_type.name} - {faction.name}")
    setup_render_pair(unit_type, faction)

    def save_and_continue():
        save_current_preview(unit_type, faction)
        global current_index
        current_index += 1
        invoke(render_next, delay=0.01)

    invoke(save_and_continue, delay=render_delay)

render_next()
app.run()
