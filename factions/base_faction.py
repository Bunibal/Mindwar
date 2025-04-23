import json
from enum import Enum, auto

from ursina import *

from buildings.base_building import BaseBuilding
from cards.base_card import BaseCard
from units.base_unit import BaseUnit


class FactionType(Enum):
    HUMAN = auto()
    ORC = auto()
    WIZARD = auto()
    ELVE = auto()
    DWARVE = auto()
    UNDEAD = auto()
    DEMON = auto()

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
        self.faction_type = faction_type
        self.description = faction_config.description
        self.color = color.white
        self.resources = faction_config.resources
        self.units = faction_config.units
        self.buildings = faction_config.buildings
        self.cards = []

    def add_card(self, card: BaseCard):
        self.cards.append(card)

    def play_card(self, card: BaseCard):
        if card in self.cards:
            card.play_card()
            self.cards.remove(card)
        else:
            print(f"Card {card} not found in inventory {self.name}.")

    def move_unit(self, unit, new_grid_position):
        if unit in self.units:
            if unit.grid_position == new_grid_position:
                print(f"Unit {unit} is already at the desired grid position.")
                return
            unit.move_unit(new_grid_position)
        else:
            print(f"Unit {unit} not found in faction {self.name}.")

    def create_unit(self, unit_type, position):
        unit = BaseUnit(position, self.faction_type, unit_type)
        self.units.append(unit)
        return unit

    def destroy_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)
            unit.destroy_unit()
        else:
            print(f"Unit {unit} not found in faction {self.name}.")

    def create_building(self, building_type, grid_position):
        building = BaseBuilding(grid_position, self.faction_type, building_type)
        self.buildings.append(building)
        return building

    def damage_building(self, building, damage):
        if building in self.buildings:
            building.damage_building(damage)
        else:
            print(f"Building {building} not found in faction {self.name}.")

    def destroy_building(self, building):
        if building in self.buildings:
            building.destroy_building()
            self.buildings.remove(building)
        else:
            print(f"Building {building} not found in faction {self.name}.")
