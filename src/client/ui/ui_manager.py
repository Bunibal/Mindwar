from ursina import *
import ast

from src.entities.factions.base_faction import BaseFaction
from src.entities.factions.base_faction import FactionType
from src.entities.tiles.terrain_type import TerrainType
from src.entities.units.base_unit import BaseUnitUI, UnitType
from src.map.map_manager import MapManager


class UIManager:
    def __init__(self, rcp_peer):
        self.is_prepare_random_map = None
        self.map_load_filepath = None
        self.slots = None
        self.col_input = None
        self.action_field_input = None
        self.edge_input = None
        self.row_input = None
        self.rcp_peer = rcp_peer
        self.menu_panel = None
        self.editor_toolbar = None
        self.popup = None

        # Lobby UI state
        self.lobby_panel = None
        self.lobby_list_container = None
        self.current_lobbies = []
        self.current_lobby_id = None
        self.player_id = None
        self.server_ip = "192.168.1.179"
        self.server_port = 8080
        self.is_connected = False

    def start_menu(self):
        window.title = "Mindwar - Main Menu"
        self.menu_panel = Entity(
            parent=camera.ui,
            model='quad',
            texture='../assets/ui/menu_background.png',
            scale=(1.6, 0.9),
            color=color.rgba(50, 50, 50, 180),
            position=(0, 0, 0),
            origin=(0, 0),
            z=999
        )

        button_labels = [
            'Start Game',
            'Multiplayer',
            'Start Map Editor',
            'Quit'
        ]

        for i, label in enumerate(button_labels):
            Button(
                text=label,
                parent=self.menu_panel,
                y=0.175 - i * 0.12,  # space out evenly
                scale=(0.3, 0.05),
                origin=(0, 0),
                on_click=getattr(self, self._button_callback(label))
            )

    def start_map_editor(self):
        print("🛠 Starting Map Editor...")
        destroy(self.menu_panel)
        self.menu_panel = None

        self.game_manager.generate_random_map()
        self.map_editor()

    def map_editor(self):
        self.center_camera(self.game_manager.map_manager.rows, self.game_manager.map_manager.cols)

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

    def return_to_menu(self):
        print("🔙 Returning to Main Menu...")
        if self.game_manager.map_manager:
            self.game_manager.destroy_map()
            self.game_manager.map_manager = None
        if self.editor_toolbar:
            destroy(self.editor_toolbar)
            self.editor_toolbar = None
        self.clear_ui()
        self.start_menu()

    def center_camera(self, rows, cols):
        x, y, z = self.hex_to_world(rows / 2, cols / 2)
        camera.orthographic = False
        camera.fov = 50
        camera.position = (x, y - 85, -50)
        camera.look_at(Vec3(x, y, 0))

    def _button_callback(self, label):
        return {
            'Start Game': 'start_game_locally',
            'Multiplayer': 'show_connection_screen',
            'Start Map Editor': 'start_map_editor',
            'Random Map': 'generate_random_map',
            'Save Map': 'save_current_map',
            'Load Map': 'load_map_from_file',
            'Quit': 'quit_game'
        }[label]

    def get_server(self, raise_error=True):
        conns = self.rcp_peer.get_connections()
        if conns:
            return conns[0]
        if raise_error:
            raise Exception("No server connection available.")
        return None
    
    def start_game_locally(self):
        print(type(self.get_server()))
        self.rcp_peer.start_game(self.get_server())

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
        self.game_manager.map_manager.save("maps/" + filename + ".json")
        print(f"💾 Map saved to maps/{filename}.json")
        self.close_popup()

    def close_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)
            self.popup = None

    def open_load_popup(self, load_map=True):
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
                    on_click=Func(self.load_selected_map if load_map else self.prepare_load_map,
                                  os.path.join(map_dir, file))
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
        if self.game_manager.map_manager:
            self.game_manager.destroy_map()
        self.game_manager.map_manager = MapManager()
        try:
            self.game_manager.map_manager.load(filepath)
            self.game_manager.gamestate.game_map = self.game_manager.game_map
            self.game_manager.gamestate.game_state = "game"

            print(f"📂 Loaded map: {filepath}")
            self.close_popup()
            self.map_editor()
        except Exception as e:
            print(f"❌ Failed to load map: {e}")

    def open_generate_random_map_popup(self, load_map=True):
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
            Text(f"{label}:", parent=panel, x=-0.25, y=y + 0.02, origin=(-0.5, 0), scale=0.7, color=color.black,
                 z=-1)
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
            on_click=Func(self.confirm_generate_random_map, load_map)
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

    def confirm_generate_random_map(self, load_map):
        if load_map:
            try:
                rows = int(self.row_input.text)
                cols = int(self.col_input.text)
                n_action_fields = int(self.action_field_input.text)
                n_streets = int(self.edge_input.text)
                weights = {
                    terrain: float(input_field.text)
                    for terrain, input_field in self.terrain_weight_inputs.items()
                }

                self.game_manager.generate_random_map(
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
        else:
            self.is_prepare_random_map = True

    @staticmethod
    def hex_to_world(q, r):
        tile_width = -2
        dx = sqrt(3)  # ≈ 1.732, horizontal spacing
        dy = tile_width - 1

        x = r * dx * 2 + (q % 2) * dx
        y = q * dy

        return (x, y, 0)

    def clear_ui(self):
        for child in camera.ui.children:
            destroy(child)

    def setup_game_ui(self):
        self.clear_ui()

        # Add proper lighting for the faction selection screen
        DirectionalLight().look_at(Vec3(1, -1, -1))
        AmbientLight(color=color.rgba(120, 120, 120, 0.5))  # Add ambient light for better visibility

        self.slots = []
        self.factions = [BaseFaction(name=faction.name, faction_type=faction) for faction in FactionType]

        title = Text("Choose Your Factions", parent=camera.ui, y=0.45, scale=2, origin=(0, 0), color=color.white)
        start_index = [0, -1, -1, -1]

        # Faction slots (up to 4)
        for i in range(4):
            x_pos = -0.5 + i * 0.33
            slot = Entity(parent=camera.ui, position=(x_pos, 0), scale=(0.4, 0.6), model='quad',
                          color=color.gray.tint(0.2), z=0.1)

            slot.current_faction_index = start_index[i]

            # Faction name label
            slot.faction_label = Text(
                text=self.factions[slot.current_faction_index].name,
                parent=slot,
                y=0.35,
                scale=1.5,
                origin=(0, 0),
                color=color.black,
                z=-0.1
            )

            # Arrow buttons
            left = Button(text='Back', parent=slot, position=(-0.18, -0.35, -0.1), scale=(0.3, 0.1), color=color.azure)
            right = Button(text='Forward', parent=slot, position=(0.18, -0.35, -0.1), scale=(0.3, 0.1),
                           color=color.azure)

            # Model display - Remove color override here too
            slot.model_display = BaseUnitUI(
                position=(0, -0.1, 0.3),
                faction=FactionType.HUMAN.name,
                unit_type=UnitType.INFANTRY,
                parent=scene,
                owner=self.factions[slot.current_faction_index],
                scale=(0.3, 0.3, 0.3),
                rotation_y=180,
                z=-1
                # REMOVED any color parameter to preserve model colors
            )

            def update_model(s=slot):
                faction = self.factions[s.current_faction_index]
                s.faction_label.text = faction.name
                s.model_display.owner = faction.name
                s.model_display.model = BaseUnitUI.get_model_for_unit(slot.model_display.type, faction.name)
                # Don't set color here either - let the model keep its original colors

            left.on_click = Func(self.prev_faction, slot, update_model)
            right.on_click = Func(self.next_faction, slot, update_model)

            self.slots.append(slot)

        # Control Buttons
        button_y = -0.45

        start_game_btn = Button(
            text='Start Game',
            position=(0.5, button_y),
            scale=(0.25, 0.1),
            parent=camera.ui,
            color=color.lime,
            on_click=self.ui_start_game_locally
        )

        back_btn = Button(
            text='Back to Main Menu',
            position=(-0.5, button_y),
            scale=(0.25, 0.1),
            parent=camera.ui,
            color=color.red,
            on_click=self.return_to_menu
        )

        load_map_btn = Button(
            text='Load Map',
            position=(0, button_y + 0.08),
            scale=(0.2, 0.08),
            parent=camera.ui,
            color=color.orange,
            on_click=self.open_load_popup
        )

        generate_map_btn = Button(
            text='Generate Random Map',
            position=(0, button_y),
            scale=(0.3, 0.08),
            parent=camera.ui,
            color=color.cyan,
            on_click=self.open_generate_random_map_popup
        )

    def prev_faction(self, slot, update_func):
        slot.current_faction_index = (slot.current_faction_index - 1) % len(self.factions)
        update_func()

    def next_faction(self, slot, update_func):
        slot.current_faction_index = (slot.current_faction_index + 1) % len(self.factions)
        update_func()

    def prepare_load_map(self, filepath):
        self.close_popup()
        self.map_load_filepath = filepath

    def ui_start_game_locally(self):
        # get factions chosen
        self.game_manager.chosen_factions = []
        for slot in self.slots:
            if slot.current_faction_index != -1:
                self.game_manager.chosen_factions.append(self.factions[slot.current_faction_index])
        self.game_manager.n_players = len(self.game_manager.chosen_factions)
        if not self.game_manager.n_players:
            print("⚠️ No factions selected.")
            return
        self.game_manager.gamestate.game_state = "game"
        self.game_manager.gamestate.chosen_factions = self.game_manager.chosen_factions
        self.game_manager.gamestate.n_players = self.game_manager.n_players
        if self.is_prepare_random_map:
            self.game_manager.generate_random_map(
                rows=int(self.row_input.text),
                cols=int(self.col_input.text),
                n_action_fields=int(self.action_field_input.text),
                n_streets=int(self.edge_input.text),
                weights={
                    terrain: float(input_field.text)
                    for terrain, input_field in self.terrain_weight_inputs.items()
                }
            )
            self.game_manager.start_game_locally()
            self.is_prepare_random_map = False
        elif self.map_load_filepath:
            self.map_load_filepath = None
            self.game_manager.load_selected_map(self.map_load_filepath)
            self.game_manager.start_game_locally()
        else:
            self.clear_ui()
            self.game_manager.generate_random_map()
            self.center_camera(self.game_manager.map_manager.rows, self.game_manager.map_manager.cols)
            self.game_manager.start_game_locally()

    def game_ui(self):
        self.ui_elements = []
        toolbar_bg = Entity(
            parent=camera.ui,
            model='quad',
            scale=(1.3, 0.18),  # Width, height of toolbar
            position=(0, -0.48),  # Bottom center
            color=color.dark_gray
        )
        self.ui_elements.append(toolbar_bg)

        # === Player Turn Text ===
        self.turn_info = Text(
            text=f"{self.game_manager.current_player.name} – potential name's Turn",
            parent=camera.ui,
            position=(-0.6, -0.43),
            origin=(-0.5, 0),
            scale=1.3,
            color=color.white
        )
        self.ui_elements.append(self.turn_info)

        self.resources_info = Entity(
            parent=camera.ui,
            model='quad',
            scale=(0.2, 0.6),
            position=(0.8, 0.1),
            color=color.gray,
            z=-10
        )

        for i, element in enumerate(self.game_manager.current_player.resources):
            Text(
                text=f"{element['name']} : {element['amount']}",
                parent=self.resources_info,
                position=(-0.25, -0.4 + i * (1 / len(self.game_manager.current_player.resources))),
                color=color.white,
                scale=3,
                z=-9
            )

        # === Action Buttons ===
        action_labels = ['Build', 'Recruit', 'Fight', 'Move', 'Gather', 'End Turn']
        action_callbacks = [self.game_manager.build_action, self.game_manager.recruit_action,
                            self.game_manager.fight_action, self.game_manager.move_action,
                            self.game_manager.gather_action, self.game_manager.end_turn]

        for i, (label, callback) in enumerate(zip(action_labels, action_callbacks)):
            btn = Button(
                text=label,
                parent=camera.ui,
                position=(-0.6 + i * 0.23, -0.3),  # Even spacing
                scale=(0.2, 0.1),
                color=color.azure,
                on_click=callback
            )
            self.ui_elements.append(btn)

    def update_game_ui(self):
        self.update_turn_info()
        self.update_resources_info()

    def update_turn_info(self):
        if hasattr(self, 'turn_info') and self.turn_info:
            self.turn_info.text = f"{self.game_manager.current_player.name} – potential name's Turn"

    def update_resources_info(self):
        if hasattr(self, "resources_info") and self.resources_info:
            # Clear out old children (texts) first
            for child in self.resources_info.children:
                destroy(child)

            # Recreate updated resource texts
            for i, element in enumerate(self.game_manager.current_player.resources):
                Text(
                    text=f"{element['name']} : {element['amount']}",
                    parent=self.resources_info,
                    position=(-0.25, -0.4 + i * (1 / len(self.game_manager.current_player.resources))),
                    color=color.white,
                    scale=3,
                    z=-9
                )

    def game_exit_popup(self):
        if hasattr(self, 'popup') and self.popup:
            destroy(self.popup)

        self.popup = Entity(parent=camera.ui)

        # Center panel
        panel = Entity(
            parent=self.popup,
            model='quad',
            color=color.light_gray,
            scale=(0.4, 0.6),
            z=0
        )

        y = 0.4
        spacing = 0.07

        # Generate button
        Button(
            text="Exit to main menu",
            parent=panel,
            y=y - 0.1,
            x=0,
            scale=(0.6, 0.07),
            z=-1,
            on_click=Func(self.return_to_menu)
        )

        Button(
            text="Cancel",
            parent=panel,
            y=y - 0.2,
            x=0,
            scale=(0.6, 0.07),
            z=-1,
            on_click=Func(self.close_popup)
        )

    # ===== LOBBY UI METHODS =====

    def show_connection_screen(self):
        """Show connection screen with server IP/port input"""
        self.clear_ui()
        window.title = "Mindwar - Connect to Server"

        # Main panel
        self.lobby_panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(40, 40, 50, 220),
            scale=(0.8, 0.9),
            position=(0, 0),
            z=0
        )

        Text(
            text="Connect to Server",
            parent=self.lobby_panel,
            y=0.4,
            scale=2,
            origin=(0, 0),
            color=color.white
        )

        # Server IP input
        Text(
            text="Server IP:",
            parent=self.lobby_panel,
            x=-0.25,
            y=0.2,
            origin=(-0.5, 0),
            scale=1,
            color=color.light_gray
        )
        self.server_ip_input = InputField(
            parent=self.lobby_panel,
            default_value=self.server_ip,
            x=0.1,
            y=0.2,
            scale=(0.35, 0.08)
        )

        # Server Port input
        Text(
            text="Port:",
            parent=self.lobby_panel,
            x=-0.25,
            y=0.05,
            origin=(-0.5, 0),
            scale=1,
            color=color.light_gray
        )
        self.server_port_input = InputField(
            parent=self.lobby_panel,
            default_value=str(self.server_port),
            x=0.1,
            y=0.05,
            scale=(0.35, 0.08)
        )

        # Connection status text
        self.connection_status_text = Text(
            text="Not Connected",
            parent=self.lobby_panel,
            y=-0.1,
            scale=1.2,
            color=color.red,
            origin=(0, 0)
        )

        # Connect button
        Button(
            text="Connect",
            parent=self.lobby_panel,
            y=-0.25,
            scale=(0.3, 0.08),
            color=color.lime,
            on_click=self.connect_to_server
        )

        # Back button
        Button(
            text="Back to Main Menu",
            parent=self.lobby_panel,
            y=-0.38,
            scale=(0.3, 0.08),
            color=color.gray,
            on_click=self.return_from_lobby
        )

    def connect_to_server(self):
        """Attempt to connect to the server"""
        self.server_ip = self.server_ip_input.text.strip()
        try:
            self.server_port = int(self.server_port_input.text.strip())
        except ValueError:
            self.connection_status_text.text = "Invalid port number"
            self.connection_status_text.color = color.red
            return

        self.rcp_peer.start(self.server_ip, self.server_port, is_host=False)
        if self.rcp_peer.is_running():
            self.is_connected = True
            self.connection_status_text.text = f"Connected to {self.server_ip}:{self.server_port}"
            self.connection_status_text.color = color.lime
            print(f"Connected to server at {self.server_ip}:{self.server_port}")

            # Wait a moment for connection to establish, then show lobby browser
            invoke(self.show_lobby_browser, delay=0.5)
        else:
            self.connection_status_text.text = f"Connection failed."
            self.connection_status_text.color = color.red
            print(f"Failed to connect to server at {self.server_ip}:{self.server_port}")

    def show_lobby_browser(self):
        """Show the lobby browser with list of available lobbies"""
        self.clear_ui()
        window.title = "Mindwar - Lobby Browser"

        # Main panel
        self.lobby_panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(40, 40, 50, 220),
            scale=(1.4, 0.9),
            position=(0, 0),
            z=0
        )

        # Title
        Text(
            text="Available Lobbies",
            parent=self.lobby_panel,
            y=0.42,
            scale=2,
            origin=(0, 0),
            color=color.white
        )

        # Connection status
        Text(
            text=f"Connected to {self.server_ip}:{self.server_port}",
            parent=self.lobby_panel,
            y=0.35,
            scale=0.8,
            origin=(0, 0),
            color=color.lime
        )

        # Lobby list container
        self.lobby_list_container = Entity(parent=self.lobby_panel, y=0.1)

        # Initially show "Loading..." text
        Text(
            text="Loading lobbies...",
            parent=self.lobby_list_container,
            y=0,
            color=color.light_gray
        )

        # Buttons at the bottom
        Button(
            text="Create Lobby",
            parent=self.lobby_panel,
            y=-0.38,
            x=-0.2,
            scale=(0.25, 0.08),
            color=color.cyan,
            on_click=self.open_create_lobby_popup
        )

        Button(
            text="Refresh",
            parent=self.lobby_panel,
            y=-0.38,
            x=0.2,
            scale=(0.25, 0.08),
            color=color.orange,
            on_click=self.refresh_lobby_list
        )

        Button(
            text="Disconnect",
            parent=self.lobby_panel,
            y=-0.38,
            x=0.6,
            scale=(0.25, 0.08),
            color=color.red,
            on_click=self.disconnect_from_server
        )

        # Request lobby list from server
        self.refresh_lobby_list()

    def refresh_lobby_list(self):
        """Request updated lobby list from server"""
        try:
            server = self.get_server(raise_error=False)
            if server:
                self.rcp_peer.get_lobby_list(server)
                print("Requesting lobby list from server...")
            else:
                print("No server connection available")
        except Exception as e:
            print(f"Error requesting lobby list: {e}")

    def lobby_list_received(self, lobbies: list):
        """Called when server sends lobby list"""
        print(f"Received {len(lobbies)} lobbies")
        self.current_lobbies = lobbies

        # Clear the lobby list container
        if self.lobby_list_container:
            for child in self.lobby_list_container.children:
                destroy(child)

            if not lobbies:
                Text(
                    text="No lobbies available. Create one!",
                    parent=self.lobby_list_container,
                    y=0,
                    color=color.light_gray
                )
            else:
                # Display each lobby
                for i, lobby_str in enumerate(lobbies):
                    try:
                        # Parse the lobby dict string
                        lobby_dict = ast.literal_eval(lobby_str)
                        lobby_name = lobby_dict.get('name', 'Unknown')
                        lobby_id = lobby_dict.get('id', 'unknown')
                        current_players = lobby_dict.get('current_players', 0)
                        max_players = lobby_dict.get('max_players', 4)

                        # Create lobby entry button
                        lobby_btn = Button(
                            text=f"{lobby_name} ({current_players}/{max_players})",
                            parent=self.lobby_list_container,
                            y=0.15 - i * 0.12,
                            scale=(0.6, 0.1),
                            color=color.azure if current_players < max_players else color.gray,
                            on_click=Func(self.join_lobby, lobby_id) if current_players < max_players else None
                        )
                    except Exception as e:
                        print(f"Error parsing lobby: {e}")

    def open_create_lobby_popup(self):
        """Open popup to create a new lobby"""
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
            scale=(0.6, 0.5),
            z=0
        )

        Text(
            text="Create New Lobby",
            parent=panel,
            y=0.2,
            scale=1.5,
            origin=(0, 0),
            color=color.white
        )

        # Lobby name input
        Text(
            text="Lobby Name:",
            parent=panel,
            x=-0.2,
            y=0.05,
            origin=(-0.5, 0),
            scale=1,
            color=color.black
        )
        self.lobby_name_input = InputField(
            default_value='My Lobby',
            parent=panel,
            x=0.1,
            y=0.05,
            scale=(0.4, 0.08)
        )

        # Max players input
        Text(
            text="Max Players:",
            parent=panel,
            x=-0.2,
            y=-0.1,
            origin=(-0.5, 0),
            scale=1,
            color=color.black
        )
        self.max_players_input = InputField(
            default_value='4',
            parent=panel,
            x=0.1,
            y=-0.1,
            scale=(0.4, 0.08)
        )

        # Create button
        Button(
            text='Create',
            parent=panel,
            y=-0.3,
            x=-0.1,
            scale=(0.25, 0.08),
            color=color.lime,
            on_click=self.confirm_create_lobby
        )

        # Cancel button
        Button(
            text='Cancel',
            parent=panel,
            y=-0.3,
            x=0.15,
            scale=(0.25, 0.08),
            on_click=self.close_popup
        )

    def confirm_create_lobby(self):
        """Send create lobby request to server"""
        lobby_name = self.lobby_name_input.text.strip()
        if not lobby_name:
            print("Lobby name cannot be empty")
            return

        try:
            max_players = int(self.max_players_input.text.strip())
            if max_players < 2 or max_players > 8:
                print("Max players must be between 2 and 8")
                return
        except ValueError:
            print("Invalid max players number")
            return

        try:
            server = self.get_server()
            self.rcp_peer.create_lobby(server, lobby_name, max_players)
            print(f"Creating lobby: {lobby_name} with {max_players} max players")
            self.close_popup()
            # Refresh the lobby list after a short delay
            invoke(self.refresh_lobby_list, delay=0.5)
        except Exception as e:
            print(f"Error creating lobby: {e}")

    def join_lobby(self, lobby_id):
        """Join a specific lobby"""
        try:
            server = self.get_server()
            self.current_lobby_id = lobby_id
            self.rcp_peer.join_lobby(server, lobby_id, str(self.player_id))
            print(f"Joining lobby {lobby_id}")
            # Show lobby detail screen
            self.show_lobby_detail()
        except Exception as e:
            print(f"Error joining lobby: {e}")

    def show_lobby_detail(self):
        """Show detailed view of current lobby"""
        self.clear_ui()
        window.title = "Mindwar - Lobby"

        # Main panel
        self.lobby_panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(40, 40, 50, 220),
            scale=(1.2, 0.9),
            position=(0, 0),
            z=0
        )

        # Title
        self.lobby_title_text = Text(
            text="Lobby",
            parent=self.lobby_panel,
            y=0.42,
            scale=2,
            origin=(0, 0),
            color=color.white
        )

        # Player list container
        self.lobby_player_list = Entity(parent=self.lobby_panel, y=0.1)

        Text(
            text="Waiting for lobby info...",
            parent=self.lobby_player_list,
            y=0,
            color=color.light_gray
        )

        # Buttons
        Button(
            text="Ready",
            parent=self.lobby_panel,
            y=-0.38,
            x=-0.3,
            scale=(0.25, 0.08),
            color=color.lime,
            on_click=self.set_ready
        )

        Button(
            text="Not Ready",
            parent=self.lobby_panel,
            y=-0.38,
            x=0,
            scale=(0.25, 0.08),
            color=color.orange,
            on_click=self.set_not_ready
        )

        Button(
            text="Leave Lobby",
            parent=self.lobby_panel,
            y=-0.38,
            x=0.3,
            scale=(0.25, 0.08),
            color=color.red,
            on_click=self.leave_lobby
        )

    def lobby_info_received(self, lobby_info: str):
        """Called when server sends lobby info"""
        print(f"Received lobby info: {lobby_info}")
        # TODO: Parse and display lobby info
        # Update lobby_title_text and lobby_player_list

    def set_ready(self):
        """Set player status to ready"""
        try:
            server = self.get_server()
            self.rcp_peer.set_ready_status(server, True)
            print("Set ready status: True")
        except Exception as e:
            print(f"Error setting ready status: {e}")

    def set_not_ready(self):
        """Set player status to not ready"""
        try:
            server = self.get_server()
            self.rcp_peer.set_ready_status(server, False)
            print("Set ready status: False")
        except Exception as e:
            print(f"Error setting ready status: {e}")

    def leave_lobby(self):
        """Leave current lobby"""
        try:
            server = self.get_server()
            self.rcp_peer.leave_lobby(server)
            self.current_lobby_id = None
            print("Left lobby")
            # Return to lobby browser
            self.show_lobby_browser()
        except Exception as e:
            print(f"Error leaving lobby: {e}")

    def disconnect_from_server(self):
        """Disconnect from server and return to connection screen"""
        try:
            # TODO: Properly close connection
            self.is_connected = False
            self.current_lobby_id = None
            print("Disconnected from server")
            self.show_connection_screen()
        except Exception as e:
            print(f"Error disconnecting: {e}")

    def return_from_lobby(self):
        """Return to main menu from lobby system"""
        if self.lobby_panel:
            destroy(self.lobby_panel)
            self.lobby_panel = None
        self.start_menu()


def input_handle(key, ui_manager: UIManager):
    if key == 'escape':
        if ui_manager.game_manager.gamestate.game_state == "game":
            ui_manager.game_exit_popup()
