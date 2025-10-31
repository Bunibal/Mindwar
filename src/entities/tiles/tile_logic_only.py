import settings
from entities.tiles.feature_type import FeatureType
from entities.tiles.terrain_type import TerrainType


class BaseTileLogic:
    def __init__(self, grid_position=(0, 0), terrain=TerrainType.GRASSLAND, feature=FeatureType.NONE, **kwargs):
        if type(terrain) != TerrainType and terrain in TerrainType.__members__:
            self.terrain = TerrainType[terrain]
        else:
            self.terrain = terrain
        if type(feature) != FeatureType and feature in FeatureType.__members__:
            self.feature = FeatureType[feature]
        else:
            self.feature = feature
        self.owner = None
        self.buildings = []
        self.units = []
        self.grid_position = grid_position
        self.has_street = False
        self.street_rotation = None
        self.street_dirs = [(None, None), (None, None)]
        self.is_action_field = False

    @staticmethod
    def get_terrain_height(terrain):
        return {
            TerrainType.GRASSLAND: 0.1,
            TerrainType.FOREST: 0.1,
            TerrainType.WETLAND: 0.05,
            TerrainType.MOUNTAIN: 2.5,
            TerrainType.DESERT: 0.1,
            TerrainType.WATER: 0.05,
        }.get(terrain, 0.1)

    def mark_as_action_field(self):
        if self.is_action_field:
            return  # already marked

        self.is_action_field = True

    def clear_action_field(self):
        self.is_action_field = False
        if self.action_field_highlight:
            self.action_field_highlight = None

