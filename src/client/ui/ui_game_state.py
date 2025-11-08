from entities.units.base_unit import BaseUnitUI
from map.map_manager import MapManagerUI


class GameStateUI:
    def __init__(self, ui_manager):
        self.current_player = None
        self.units = []  # List of serialized units
        self.units_by_id = {}
        self.factions = {}  # player_id: faction_type
        self.game_map = None  # List of serialized map tiles
        self.map_manager = MapManagerUI()
        self.ui_manager = ui_manager

    def load_game_state(self, game_state: dict):
        self.current_player = game_state.get("current_player")
        self.unit_data = game_state.get("units", [])
        self.factions = game_state.get("factions", {})
        self.game_map = game_state.get("map", [])
        self.create_unit_models()

    def create_unit_models(self):
        self.units = []
        self.units_by_id = {}
        for unit_data in self.unit_data:
            unit = BaseUnitUI(self.ui_manager, unit_data)
            self.units.append(unit)
            self.units_by_id[unit.unit_id] = unit

    def move_unit_by_id(self, unit_id: int, new_grid_position: tuple[int, int]):
        unit = self.units_by_id.get(unit_id, None)
        if unit:
            unit.move_to(new_grid_position)
    
