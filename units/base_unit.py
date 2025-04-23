from ursina import *
from enum import Enum, auto


class UnitType(Enum):
    INFANTRY = auto()
    CAVALRY = auto()
    ARCHER = auto()
    MAGE = auto()
    SIEGE = auto()


class BaseUnit(Entity):
    def __init__(self, position: tuple, owner, map_manager=None, unit_type: UnitType = UnitType.INFANTRY,
                 scale=(1, 1, 1), **kwargs):
        self.grid_position = position
        self.type = unit_type
        self.owner = owner
        self.map_manager = map_manager
        self.moves_left = 2

        super().__init__(
            model=self.get_model_for_unit(unit_type, self.owner),
            scale=scale,
            position=position,
            origin=(0, 0),
            highlight_color=color.azure,
            pressed_color=color.lime,
            **kwargs
        )

    @staticmethod
    def get_model_for_unit(unit_type: UnitType, owner):
        return "assets/models/units/human_warrior.glb"  # Placeholder for actual model path
        # return "assets/models/units/{}_{}.glb".format(owner, unit_type)

    def add_unit_to_world(self, grid_position):
        self.grid_position = grid_position
        self.position = self.grid_to_world(*grid_position)
        self.map_manager.add_unit(self)

    def move_unit(self, new_position: tuple):
        self.grid_position = new_position
        self.position = self.grid_to_world(*new_position)

    def destroy_unit(self):
        self.disable()
        self.delete()


    @staticmethod
    def grid_to_world(q, r):
        tile_width = -2
        dx = sqrt(3)
        dy = tile_width - 1

        x = r * dx * 2 + (q % 2) * dx
        y = q * dy

        return (x, y, 0)

    def __repr__(self):
        return f"Unit(name={self.name}, position={self.position})"
