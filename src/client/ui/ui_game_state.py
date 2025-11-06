from entities.units.base_unit import BaseUnitUI
from map.map_manager import MapManagerUI


class GameStateUI:
    def __init__(self):
        self.current_player = None
        self.units = []  # List of serialized units
        self.factions = {}  # player_id: faction_type
        self.game_map = None  # List of serialized map tiles
        self.map_manager = MapManagerUI()

    def load_game_state(self, game_state: dict):
        self.current_player = game_state.get("current_player")
        self.unit_data = game_state.get("units", [])
        self.factions = game_state.get("factions", {})
        self.game_map = game_state.get("map", [])
        self.create_unit_models()

    def create_unit_models(self):
        self.units = []
        for unit_data in self.unit_data:
            unit = BaseUnitUI(unit_data)
            self.units.append(unit)
    
