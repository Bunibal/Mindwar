from ursina import *
from enum import Enum, auto

from factions.base_faction import FactionType
from utils import world_calculations


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnit(Entity):
    def __init__(self, grid_position: tuple, faction: FactionType, unit_type: UnitType = UnitType.INFANTRY,
                 scale=(1, 1, 1), **kwargs):
        self.grid_position = grid_position
        self.type = unit_type
        self.faction = faction
        self.moves_left = 2

        super().__init__(
            model=self.get_model_for_unit(unit_type, self.faction),
            scale=scale,
            position=world_calculations.grid_to_world(*grid_position),
            origin=(0, 0),
            highlight_color=color.azure,
            pressed_color=color.lime,
            **kwargs
        )

    @staticmethod
    def get_model_for_unit(unit_type: UnitType, faction: FactionType):
        unit_type_name = unit_type.name.lower()
        faction_name = faction.name.lower()
        return f"assets/models/units/{faction_name}/{unit_type_name}.glb"


    def move_unit(self, new_position: tuple):
        self.grid_position = new_position
        self.position = world_calculations.grid_to_world(*new_position)

    def destroy_unit(self):
        self.disable()
        self.delete()


    def __repr__(self):
        return f"Unit(name={self.name}, position={self.position})"
