from ursina import *
from ursina import Text

from math import sqrt

from tiles.terrain_type import TerrainType
from tiles.feature_type import FeatureType




class BaseTile(Button):
    def __init__(self, grid_position=(0, 0), terrain=TerrainType.GRASSLAND, feature=FeatureType.NONE, **kwargs):
        self.terrain = terrain
        self.feature = feature
        self.grid_position = grid_position
        self.owner = None
        self.has_street = False
        self.street_entity = None  # visual representation

        model = self.get_model_for_terrain(terrain)
        position = self.hex_to_world(*grid_position)

        super().__init__(
            parent=scene,
            model=model,
            scale=1,
            color=color.white,
            unlit=True,
            position=position,
            origin=(0, 0),
            highlight_color=color.azure,
            pressed_color=color.lime,
            **kwargs
        )


    @staticmethod
    def hex_to_world(q, r):
        tile_width = -2
        dx = sqrt(3)  # ≈ 1.732, horizontal spacing
        dy = tile_width - 1

        x = r * dx * 2 + (q%2) * dx
        y = q * dy

        return (x, y, 0)

    def on_click(self):
        q, r = self.grid_position
        print(f"Clicked tile at row: {q}, col: {r}")
        print(f"Tile world position: {self.x}, {self.y}")
        print(f"Tile terrain: {self.terrain}")

    def get_model_for_terrain(self, terrain):
        return {
            TerrainType.GRASSLAND: 'hex_grass.glb',
            TerrainType.FOREST: 'hex_forest.glb',
            TerrainType.WETLAND: 'hex_wetland.glb',
            TerrainType.MOUNTAIN: 'hex_mountain.glb',
            TerrainType.DESERT: 'hex_desert.glb',
            TerrainType.WATER: 'hex_water.glb',
        }.get(terrain, 'hex_grass.obj')

    def get_terrain_height(self, terrain):
        return {
            TerrainType.GRASSLAND: 0.1,
            TerrainType.FOREST: 0.1,
            TerrainType.WETLAND: 0.05,
            TerrainType.MOUNTAIN: 2.5,
            TerrainType.DESERT: 0.1,
            TerrainType.WATER: 0.05,
        }.get(terrain, 0.1)

    def get_terrain_color(self, terrain):
        return {
            TerrainType.GRASSLAND: color.green,
            TerrainType.FOREST: rgb(0, 100, 0),
            TerrainType.WETLAND: color.blue,
            TerrainType.MOUNTAIN: color.gray,
            TerrainType.DESERT: color.yellow,
            TerrainType.WATER: color.cyan,
        }.get(terrain, color.green)