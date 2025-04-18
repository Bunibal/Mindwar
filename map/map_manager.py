from ursina import *
from tiles.base_tile import BaseTile
from tiles.terrain_type import TerrainType
from tiles.feature_type import FeatureType
from tiles.feature_type import FLAT_TERRAINS
import random

class MapManager:
    def __init__(self, rows=8, cols=6):
        self.rows = rows
        self.cols = cols
        self.tiles = []

    def generate_map(self):
        for q in range(self.rows):
            for r in range(self.cols):
                terrain = self.random_terrain()
                tile = BaseTile(grid_position=(q, r), terrain=terrain)
                self.tiles.append(tile)

                if self.should_place_street():
                    tile.terrain = self.random_terrain(flat=True)
                    tile.has_street = True
                    tile.street_entity = Entity(
                        model=self.get_correct_street_model(tile),
                        parent=tile,
                        scale=0.5,
                        position=(0, 0, 0.1),
                        rotation_z=self.get_street_rot(tile),
                        unlit=True
                    )

    def should_place_street(self):
        return random.randint(0, 1) == 1

    def get_correct_street_model(self, tile):
        return random.choice(["assets/models/hex_streets/street_straight.glb",
                              "assets/models/hex_streets/street_curve_small.glb",
                              "assets/models/hex_streets/street_curve_large.glb"])

    def random_terrain(self, flat=False):
        if flat:
            terrain_types = list(FLAT_TERRAINS)
            return random.choice(terrain_types)
        else:
            terrain_types = list(TerrainType)
            return random.choice(terrain_types[1:])

    def get_street_rot(self, tile):
        return random.choice([0, 60, 120])


