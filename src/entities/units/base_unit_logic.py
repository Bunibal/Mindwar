from enum import Enum, auto

from src import settings
from src.utils import world_calculations


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnit:
    def __init__(self, faction: str, unit_type: UnitType,
                 scale=19, grid_position: tuple = (0, 0), position: tuple = None, rotation=(90, 0, 180)):
        self.grid_position = grid_position
        self.type = unit_type
        self.faction = faction.lower()
        self.moves_left = 2
        print(f"Unit created: {self.model}")
        print(f"Texture: {self.texture}")
        print(f"Color: {self.color}")
        print(f"Unlit: {self.unlit}")
        self.on_the_map = True


    def move_unit(self, new_position: tuple):
        self.grid_position = new_position
        self.position = world_calculations.grid_to_world(*new_position)

    def destroy_unit(self):
        self.on_the_map = False
        
    def __str__(self):
        return f"Unit(unit_type={self.type}, unit_faction={self.faction}, grid_position={self.grid_position})"
