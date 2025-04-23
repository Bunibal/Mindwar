from enum import Enum, auto

from ursina import Entity, color

from factions.base_faction import FactionType
from utils import world_calculations


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
    def __init__(self, grid_position: tuple, faction: FactionType, building_type: BuildingType = BuildingType.BARRACKS,
                 scale=(1, 1, 1), **kwargs):
        self.grid_position = grid_position
        self.type = building_type
        self.faction = faction
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
        print(f"{self} added to world at {grid_position}")

    def __repr__(self):
        return f"Building(type={self.type}, owner={self.faction})"

    def damage_building(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.destroy_building()
            print(f"{self} destroyed.")

    @staticmethod
    def get_model_for_building(building_type: BuildingType, faction: FactionType):
        building_type_name = building_type.name.lower()
        faction_name = faction.name.lower()
        return f"assets/models/buildings/{faction_name}/{building_type_name}.glb"

    def destroy_building(self):
        self.disable()
        self.delete()