from enum import Enum, auto

from entities.factions.base_faction import FactionType
from src import settings
from src.utils import world_calculations


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnitLogic:
    def __init__(self, faction: FactionType, unit_type: UnitType,
                 grid_position: tuple = (0, 0)):
        self.grid_position = grid_position
        self.type = unit_type
        self.faction = faction.lower()
        self.moves_left = 2
        print(f"Unit created: {self.model}")
        print(f"Texture: {self.texture}")
        print(f"Color: {self.color}")
        print(f"Unlit: {self.unlit}")
        self.on_the_map = True

    def update(self, payload):
        pass

    def move_unit(self, new_position: tuple):
        self.grid_position = new_position


    def destroy_unit(self):
        self.on_the_map = False

    def __str__(self):
        return f"Unit(unit_type={self.type}, unit_faction={self.faction}, grid_position={self.grid_position})"
