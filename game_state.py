from ursina import DirectionalLight, Vec3, AmbientLight, color

from map import map_manager

class Game_state:
    def __init__(self):
        self.player = None
        self.map_manager = map_manager.MapManager(rows=10, cols=20)
        self.game_map = None
        self.game_objects = []
        self.game_state = "menu"
        self.difficulty = "easy"

    def update_map(self, action):
        self.map_manager.update(action)

    def generate_game(self):
        # Generate game content
        self.map_manager.generate_map()

        # Lighting
        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        AmbientLight(color=color.rgba(120, 120, 120, 0.5))
