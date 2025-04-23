import json
from enum import Enum, auto

from ursina import *



class FactionType(Enum):
    HUMANS = 'humans'
    ORCS = 'orcs'
    WIZARDS = 'wizards'
    ELVES = 'elves'
    DWARVES = 'dwarves'
    UNDEAD = 'undead'
    DEMONS = 'demons'
    NONE = 'none'

class BuildingType(Enum):
    BARRACKS = 'barracks'
    TOWER = 'tower'
    FARM = 'farm'
    MINE = 'mine'
    CASTLE = 'castle'

class Building:
    def __init__(self, position: tuple, building_type: str = 'basic'):
        self.position = position
        self.type = building_type
        self.color = color.white
        self.health = 100

    def __repr__(self):
        return f"Building(position={self.position}, type={self.type})"



def _load_faction_config(faction_type: FactionType) -> dict:
    with open('configs/factions_config.json', 'r') as f:
        config = json.load(f)

    for faction in config['factions']:
        if faction['faction_type'] == faction_type.value:
            return faction  # Return the entire faction configuration
    return {}


class BaseFaction:
    # move, initiate combat(unit or building), build building, gather resources, recruit unit, draw card
    def __init__(self, name: str, faction_type: FactionType):
        faction_config = _load_faction_config(faction_type)
        self.name = name
        self.description = faction_config.description
        self.color = color.white
        self.resources = faction_config.resources
        self.units = faction_config.units
        self.buildings = faction_config.buildings

    def move_unit(self, unit, new_position):
        if unit in self.units:
            if unit.position == new_position:
                print(f"Unit {unit} is already at the desired position.")
                return
            unit.position = new_position
        else:
            print(f"Unit {unit} not found in faction {self.name}.")

    def add_unit(self, unit, position):
        self.units.append(unit)
        unit.position = position
        unit.faction = self.name
        unit.color = self.color
        unit.update_model()

    def remove_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)
            unit.faction = None
            unit.color = color.white
            unit.update_model()
        else:
            print(f"Unit {unit} not found in faction {self.name}.")

    def add_building(self, building):
        self.buildings.append(building)

    def damage_building(self, building, damage):
        if building in self.buildings:
            building.health -= 10
            if building.health <= 0:
                self.destroy_building(building)
        else:
            print(f"Building {building} not found in faction {self.name}.")

    def destroy_building(self, building):
        if building in self.buildings:
            self.buildings.remove(building)
        else:
            print(f"Building {building} not found in faction {self.name}.")
