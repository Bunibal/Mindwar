from ursina import *
import os
from game_state import Game_state
from tiles.base_tile import BaseTile
from ursina import camera, Vec3
from map import map_manager
from tiles.terrain_type import TerrainType


class GameManager:
    def __init__(self):
        self.map_manager = None
        self.menu_panel = None
        self.gamestate = Game_state()
        self.gamestate.game_manager = self
        self.start_menu()

    def start_menu(self):
        window.title = "Mindwar - Main Menu"
        self.menu_panel = Entity(
            parent=camera.ui,
            model='quad',
            texture='assets/ui/menu_background.png',
            scale=(1.6, 0.9),
            color=color.rgba(50, 50, 50, 180),
            position=(0, 0, 0),
            origin=(0, 0),
            z=999
        )

        button_labels = [
            'Start Map Editor',
            'Quit'
        ]

        for i, label in enumerate(button_labels):
            Button(
                text=label,
                parent=self.menu_panel,
                y=0.125 - i * 0.15,  # space out evenly
                scale=(0.3, 0.05),
                origin=(0, 0),
                on_click=getattr(self, self._button_callback(label))
            )

    def start_map_editor(self):
        print("🛠 Starting Map Editor...")
        destroy(self.menu_panel)
        self.menu_panel = None

        self.generate_random_map()
        self.map_editor()

    def map_editor(self):
        self.center_camera(10, 20)


        # Create UI toolbar
        self.editor_toolbar = Entity(parent=camera.ui)

        Button(
            text='Save Map',
            parent=self.editor_toolbar,
            position=(-0.6, 0.45),
            scale=(0.15, 0.07),
            on_click=self.open_save_popup
        )

        Button(
            text='Load Map',
            parent=self.editor_toolbar,
            position=(-0.4, 0.45),
            scale=(0.15, 0.07),
            on_click=self.open_load_popup
        )

        Button(
            text="Generate Random Map",
            parent=self.editor_toolbar,
            position=(-0.1, 0.45),
            scale=(0.3, 0.07),
            on_click=self.open_generate_random_map_popup
        )

        Button(
            text="Main Menu",
            parent=self.editor_toolbar,
            position=(0.2, 0.45),
            scale=(0.15, 0.07),
            on_click=self.return_to_menu
        )

    def destroy_map(self):
        if self.editor_toolbar:
            destroy(self.editor_toolbar)
        self.editor_toolbar = None
        for tile in self.gamestate.game_map:
            destroy(tile)
        del self.map_manager
        self.map_manager = None
        self.gamestate.game_map = []
        scene.clear()

    def return_to_menu(self):
        print("🔙 Returning to Main Menu...")
        self.destroy_map()
        destroy(self.editor_toolbar)
        self.editor_toolbar = None
        self.map_manager = None
        self.start_menu()

    def center_camera(self, rows, cols):
        x, y, z = BaseTile.hex_to_world(rows / 2, cols / 2)
        camera.orthographic = False
        camera.fov = 50
        camera.position = (x, y - 85, -50)
        camera.look_at(Vec3(x, y, 0))

    def _button_callback(self, label):
        return {
            'Start Map Editor': 'start_map_editor',
            'Random Map': 'generate_random_map',
            'Save Map': 'save_current_map',
            'Load Map': 'load_map_from_file',
            'Quit': 'quit_game'
        }[label]

    def quit_game(self):
        application.quit()

    def open_save_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)

        self.popup = Entity(parent=camera.ui)

        # Background overlay
        Entity(
            parent=self.popup,
            model='quad',
            scale=2,
            color=color.rgba(0, 0, 0, 180),
            z=1
        )

        # Panel
        panel = Entity(
            parent=self.popup,
            model='quad',
            color=color.gray,
            scale=(0.6, 0.4),
            z=0
        )

        # Input for filename
        self.save_input = InputField(
            default_value='map1',
            parent=panel,
            y=0.1,
            scale=(0.5, 0.1)
        )

        # Save button
        Button(
            text='Save',
            parent=panel,
            y=-0.1,
            scale=(0.25, 0.08),
            on_click=self.confirm_save
        )

        # Cancel
        Button(
            text='Cancel',
            parent=panel,
            y=-0.25,
            scale=(0.25, 0.08),
            on_click=self.close_popup
        )

    def confirm_save(self):
        filename = self.save_input.text.strip()
        if not filename:
            print("⚠️ No filename entered.")
            return
        if not os.path.exists('maps'):
            os.makedirs('maps')
        self.map_manager.save("maps/" + filename + ".json")
        print(f"💾 Map saved to maps/{filename}.json")
        self.close_popup()

    def close_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)
            self.popup = None

    def open_load_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)

        self.popup = Entity(parent=camera.ui)

        # Background overlay
        Entity(
            parent=self.popup,
            model='quad',
            scale=2,
            color=color.rgba(0, 0, 0, 180),
            z=1
        )

        # Panel
        panel = Entity(
            parent=self.popup,
            model='quad',
            color=color.gray,
            scale=(0.6, 0.6),
            z=0
        )

        # Scrollable list of map files
        self.scroll_container = Entity(parent=panel, y=0.15)

        map_dir = 'maps'
        if not os.path.exists(map_dir):
            os.makedirs(map_dir)

        files = [f for f in os.listdir(map_dir) if f.endswith('.json')]
        if not files:
            Text("No map files found.", parent=self.scroll_container, y=0.2, color=color.red)
        else:
            for i, file in enumerate(files):
                Button(
                    text=file,
                    parent=self.scroll_container,
                    y=0.2 - i * 0.1,
                    scale=(0.5, 0.08),
                    on_click=Func(self.load_selected_map, os.path.join(map_dir, file))
                )

        # Cancel button
        Button(
            text='Cancel',
            parent=panel,
            y=-0.25,
            scale=(0.25, 0.08),
            on_click=self.close_popup
        )

    def load_selected_map(self, filepath):
        if self.map_manager:
            self.destroy_map()
        self.map_manager = map_manager.MapManager()
        try:
            self.map_manager.load(filepath)
            self.gamestate.game_map = self.game_map
            self.gamestate.game_state = "game"

            print(f"📂 Loaded map: {filepath}")
            self.close_popup()
            self.map_editor()
        except Exception as e:
            print(f"❌ Failed to load map: {e}")

    def open_generate_random_map_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)

        self.popup = Entity(parent=camera.ui)

        # Center panel
        panel = Entity(
            parent=self.popup,
            model='quad',
            color=color.light_gray,
            scale=(0.7, 0.9),
            z=0
        )

        y = 0.4
        spacing = 0.07

        def add_input(label, default, attr_name):
            nonlocal y
            Text(f"{label}:", parent=panel, x=-0.25, y=y + 0.02, origin=(-0.5, 0), scale=0.7, color=color.black, z=-1)
            input_field = InputField(
                parent=panel,
                default_value=str(default),
                y=y,
                x=0.1,
                scale=(0.25, 0.065),
                z=-1
            )
            setattr(self, attr_name, input_field)
            y -= spacing

        # Base config inputs
        add_input("Rows", 10, "row_input")
        add_input("Cols", 20, "col_input")
        add_input("Action Fields", 10, "action_field_input")
        add_input("Edges", 10, "edge_input")

        # Terrain weights
        self.terrain_weight_inputs = {}
        for terrain in TerrainType:
            if terrain.name == "NONE":
                continue
            Text(f"{terrain.name.capitalize()}:", parent=panel, x=-0.25, y=y + 0.02, origin=(-0.5, 0), scale=0.65,
                 color=color.black, z=-1)
            input_field = InputField(
                parent=panel,
                default_value="1",
                y=y,
                x=0.1,
                scale=(0.25, 0.06),
                z=-1
            )
            self.terrain_weight_inputs[terrain] = input_field
            y -= spacing * 0.85

        # Generate button
        Button(
            text="Generate",
            parent=panel,
            y=y - 0.05,
            x=-0.1,
            scale=(0.25, 0.07),
            z=-1,
            on_click=self.confirm_generate_random_map
        )

        # Cancel button
        Button(
            text="Cancel",
            parent=panel,
            y=y - 0.15,
            x=-0.1,
            scale=(0.25, 0.07),
            z=-1,
            on_click=self.close_popup
        )

    def confirm_generate_random_map(self):
        try:
            rows = int(self.row_input.text)
            cols = int(self.col_input.text)
            n_action_fields = int(self.action_field_input.text)
            n_streets = int(self.edge_input.text)
            weights = {
                terrain: float(input_field.text)
                for terrain, input_field in self.terrain_weight_inputs.items()
            }

            self.generate_random_map(
                rows=rows,
                cols=cols,
                n_action_fields=n_action_fields,
                n_streets=n_streets,
                weights=weights
            )
            self.close_popup()
            self.map_editor()
        except Exception as e:
            print(f"❌ Error generating map: {e}")

    def generate_random_map(self, rows=10, cols=20, n_action_fields=10, n_streets=20, weights=None):
        if self.map_manager:
            self.destroy_map()
        self.map_manager = map_manager.MapManager(
            rows=rows,
            cols=cols,
            n_action_fields=n_action_fields,
            n_streets=n_streets,
            terrain_weights=weights)
        self.game_map = self.map_manager.generate_map()
        self.gamestate.game_map = self.game_map

        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        AmbientLight(color=color.rgba(120, 120, 120, 0.5))
        self.gamestate.game_state = "game"
