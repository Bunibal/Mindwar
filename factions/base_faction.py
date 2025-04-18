from ursina import color


class BaseFaction:
    def __init__(self):
        self.name = "Base Faction"
        self.color = color.white
        self.start_resources = {
            "gold": 0,
            "wood": 0,
            "stone": 0,
            "food": 0,
            "arcane_power": 0
        }
        self.units = []
        self.buildings = []

    def add_unit(self, unit, position):
        self.units.append(unit)

