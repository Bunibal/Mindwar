from enum import Enum, auto

from entities.tiles.terrain_type import TerrainType

ACTION_FIELDS = {
    TerrainType.GRASSLAND,
    TerrainType.WETLAND,
    TerrainType.DESERT
}

FLAT_TERRAINS = {
    TerrainType.GRASSLAND,
    TerrainType.DESERT,
    TerrainType.WETLAND,
    TerrainType.WATER
}


class FeatureType(Enum):
    NONE = auto()
    OUTPOST = auto()
    RUINS = auto()
    RIVER = auto()
