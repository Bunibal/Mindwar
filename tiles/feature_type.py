from enum import Enum, auto
from tiles.terrain_type import TerrainType

FLAT_TERRAINS = {
    TerrainType.GRASSLAND,
    TerrainType.DESERT,
    TerrainType.WETLAND
}

class FeatureType(Enum):
    NONE = auto()
    OUTPOST = auto()
    RUINS = auto()
    RIVER = auto()
