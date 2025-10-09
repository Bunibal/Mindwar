import json
from enum import Enum, auto

from ursina import *

from src.entities.buildings.base_building import BaseBuilding, BuildingType
from src.entities.cards.base_card import BaseCard
from src.entities.units.base_unit import BaseUnitUI, UnitType


class FactionType(Enum):
    HUMAN = auto()
    ORC = auto()
    WIZARD = auto()
    ELF = auto()
    DWARF = auto()
    UNDEAD = auto()
    DEMON = auto()
    NONE = None


def _load_faction_config(faction_type: FactionType) -> dict:
    with open('src/configs/factions_config.json', 'r') as f:
        config = json.load(f)

    for faction in config['factions']:
        if faction['faction_type'] == faction_type.name.lower():
            return faction  # Return the entire faction configuration
    return {}


class BaseFaction:
    # move, initiate combat(unit or building), build building, gather resources, recruit unit, draw card
    def __init__(self, name: str, faction_type: FactionType):
        if faction_type == faction_type.NONE:
            self.name = "NONE"
            return
        faction_config = _load_faction_config(faction_type)
        self.name = name
        self.faction_type = faction_type
        self.description = faction_config['description']
        self.color = color.white
        self.resources = faction_config['resources']
        self.units_start_config = faction_config["units"]
        self.units = []
        self.buildings = []
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
        unit = BaseUnitUI(position, self.faction_type, unit_type)
        self.units.append(unit)
        return unit

    def destroy_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)
            unit.destroy_unit()
        else:
            print(f"Unit {unit} not found in faction {self.name}.")

    def create_building(self, building_type, grid_position):
        building = BaseBuilding(grid_position, self.faction_type.name, building_type)
        self.buildings.append(building)
        return building

    def damage_building(self, building, damage):
        if building in self.buildings:
            if building.damage_building(damage):
                self.destroy_building(building)
        else:
            print(f"Building {building} not found in faction {self.name}.")

    def destroy_building(self, building):
        if building in self.buildings:
            building.destroy_building()
            self.buildings.remove(building)
        else:
            print(f"Building {building} not found in faction {self.name}.")

    def __str__(self):
        buildings_str = ', '.join(str(b) for b in self.buildings)
        units_str = ', '.join(str(u) for u in self.units)
        cards_str = ', '.join(str(c) for c in self.cards)
        return f"Faction(player_name={self.name}, faction_type={self.faction_type}, buildings={buildings_str}, units={units_str}, cards={cards_str})"


if __name__ == "__main__":
    # Create a test faction
    test_faction = BaseFaction("Test Faction", FactionType.HUMAN)
    # Assert: No units, no buildings, no cards
    assert len(test_faction.units) == 0, "Faction should start with 0 units"
    assert len(test_faction.buildings) == 0, "Faction should start with 0 buildings"
    assert len(getattr(test_faction, 'cards', [])) == 0, "Faction should start with 0 cards"

    # Test unit creation and movement
    test_unit = test_faction.create_unit(UnitType.INFANTRY, (0, 0))
    # Assert: One infantry unit
    assert len(test_faction.units) == 1, "Should have 1 unit"
    assert test_faction.units[0].type == UnitType.INFANTRY, "Unit should be infantry"

    test_unit2 = test_faction.create_unit(UnitType.CAVALRY, (0, 1))
    # Assert: Two units, infantry and cavalry
    assert len(test_faction.units) == 2, "Should have 2 units"
    unit_types = {u.type for u in test_faction.units}
    assert UnitType.INFANTRY in unit_types and UnitType.CAVALRY in unit_types, "Should have infantry and cavalry"

    # Test building creation and destruction
    test_building = test_faction.create_building(BuildingType.BARRACKS, (2, 2))
    # Assert: One barracks building
    assert len(test_faction.buildings) == 1, "Should have 1 building"
    assert test_faction.buildings[0].type == BuildingType.BARRACKS, "Building should be barracks"

    test_faction.damage_building(test_building, 10)
    # Assert: Building health is 90 (assuming default is 100)
    assert test_building.health == 90, "Building health should be 90 after 10 damage"
    test_faction.damage_building(test_building, 90)
    print(test_faction)
    assert test_building.health == 0
    assert len(test_faction.buildings) == 0, "Building should be destroyed"

    # Test card management
    cards = BaseCard.load_cards()
    for card in cards:
        test_faction.add_card(card)
    # Assert: 4 cards
    assert len(test_faction.cards) == 4, "Should have 4 cards"

    test_faction.play_card(cards[0])
    assert len(test_faction.cards) == 3, "Should have 3 cards after playing one"

    print(test_faction)
    print("All tests completed successfully")
    sys.exit(0)
