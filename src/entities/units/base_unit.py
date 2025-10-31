from enum import Enum, auto

from ursina import *

import settings
from utils import world_calculations


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnitUI(Entity):
    def __init__(self, logic_obj, scale=19, rotation=(90, 0, 180), **kwargs):
        self.logic_object = logic_obj
        self.color = color.white
        self.position = world_calculations.grid_to_world(*self.logic_object.grid_position) 
        super().__init__(
            model=self.get_model_for_unit(self.logic_obj.unit_type, self.logic_obj.faction),
            scale=scale,
            position=self.position,
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

    # def move_unit(self, new_position: tuple):
    #     self.grid_position = new_position
    #     self.position = world_calculations.grid_to_world(*new_position)

    def destroy_unit(self):
        self.disable()
        self.delete()

    def __str__(self):
        return f"Unit Entity (unit_type={self.logic_object.type}, unit_faction={self.logic_object.faction}, grid_position={self.logic_object.grid_position})"
