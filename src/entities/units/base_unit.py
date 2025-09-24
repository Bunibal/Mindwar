from enum import Enum, auto

from ursina import *

from src import settings
from src.utils import world_calculations


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnit(Entity):
    def __init__(self, faction: str, unit_type: UnitType,
                 scale=19, grid_position: tuple = (0, 0), position: tuple = None, rotation=(90, 0, 180), **kwargs):
        self.grid_position = grid_position
        self.type = unit_type
        self.faction = faction.lower()
        self.moves_left = 2
        self.color = color.white

        super().__init__(
            model=self.get_model_for_unit(unit_type, self.faction),
            scale=scale,
            position=world_calculations.grid_to_world(*grid_position) if position is None else position,
            origin=(0, 0),
            rotation=rotation,
            **kwargs
        )
        print(f"Unit created: {self.model}")
        print(f"Texture: {self.texture}")
        print(f"Color: {self.color}")
        print(f"Unlit: {self.unlit}")

    @staticmethod
    def get_model_for_unit(unit_type: UnitType, faction: str):
        unit_type_name = unit_type.name.lower()
        return f"{settings.UNITS_DIR}/{faction}/{unit_type_name}.glb"

    def move_unit(self, new_position: tuple):
        self.grid_position = new_position
        self.position = world_calculations.grid_to_world(*new_position)

    def destroy_unit(self):
        self.disable()
        self.delete()

    def __str__(self):
        return f"Unit(unit_type={self.type}, unit_faction={self.faction}, grid_position={self.grid_position})"
