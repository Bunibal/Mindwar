from enum import Enum, auto

from ursina import Entity, color

from src import settings
from src.utils import world_calculations


class BuildingType(Enum):
    BARRACKS = ("Barracks", 10, 10, 20)
    GATHERING_STATION = ("Gathering Station", 2, 1, 1)
    CASTLE = ("Castle", 100, 200, 200)

    def __new__(cls, name, wood, stone, food):
        obj = object.__new__(cls)
        obj._value_ = name
        obj.wood = wood
        obj.stone = stone
        obj.food = food
        return obj


class BaseBuilding(Entity):
    def __init__(self, grid_position: tuple, faction: str, building_type: BuildingType,
                 scale=(1, 1, 1), **kwargs):
        self.grid_position = grid_position
        self.type = building_type
        self.faction = faction.lower()
        self.health = 100

        super().__init__(
            model=self.get_model_for_building(building_type, self.faction),
            scale=scale,
            position=world_calculations.grid_to_world(*grid_position),
            origin=(0, 0),
            highlight_color=color.azure,
            pressed_color=color.lime,
            **kwargs
        )

    def __str__(self):
        return f"Building(building_type={self.type}, faction={self.faction}, health={self.health}, grid_position={self.grid_position})"

    def damage_building(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.destroy_building()
            print(f"{self} destroyed.")
            return True
        return False

    @staticmethod
    def get_model_for_building(building_type: BuildingType, faction: str):
        building_type_name = building_type.name.lower()
        faction_name = faction.lower()
        return f"{settings.BUILDINGS_DIR}/{faction_name}/{building_type_name}.glb"

    def destroy_building(self):
        # TODO
        pass#
        # self.disable()
        # self.delete()