from ursina import DirectionalLight, Vec3, AmbientLight, color

from map import map_manager

class Game_state:
    def __init__(self):
        self.player = None
        self.map_manager = map_manager.MapManager(rows=10, cols=20)
        self.game_map = None
        self.game_objects = []
        self.game_state = "menu"

    def update_map(self, action):
        self.map_manager.update(action)



    def load_map_data(self, map_data):
        pass
