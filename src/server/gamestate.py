class GameState:
    def __init__(self):
        self.player = None
        self.game_map = None
        self.game_objects = []
        self.game_state = "menu"
        self.game_manager = None

    def to_dict(self):
        self.map_to_dict()

    def from_dict(self, data):
        self.map_from_dict(data)

    def map_to_dict(self):
        return {
            "map": self.game_manager.map_manager.to_dict()
        }

    def map_from_dict(self, data):
        self.game_map = self.game_manager.map_manager.from_dict(data["map"])
