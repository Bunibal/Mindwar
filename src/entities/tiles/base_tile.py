from ursina import *

import settings
from entities.tiles.feature_type import FeatureType
from entities.tiles.terrain_type import TerrainType


class BaseTileUI(Button):
    def __init__(self, logic_object, **kwargs):
        self.logic_object = logic_object

        model = self.get_model_for_terrain(self.logic_object.terrain)
        position = self.hex_to_world(*self.logic_object.grid_position)
        

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

        x = r * dx * 2 + (q % 2) * dx
        y = q * dy

        return (x, y, 0)

    def on_click(self):
        q, r = self.logic_object.grid_position
        print(f"Clicked tile at row: {q}, col: {r}")
        print(f"Tile world position: {self.x}, {self.y}")
        print(f"Tile terrain: {self.logic_object.terrain}")
        print(f"Tile feature: {self.logic_object.feature}")
        if self.has_street:
            print(f"Tile has street: {self.logic_object.street_entity}")
            print(f"Street rotation: {self.logic_object.street_rotation}")
            print(f"Street directions: {self.logic_object.street_dirs}")
            print(f"even: {self.logic_object.grid_position[0] % 2 == 0}")

    @staticmethod
    def get_model_for_terrain(terrain):
        return {
            TerrainType.GRASSLAND: f'{settings.HEX_TILES_DIR}/hex_grass.glb',
            TerrainType.FOREST: f'{settings.HEX_TILES_DIR}/hex_forest.glb',
            TerrainType.WETLAND: f'{settings.HEX_TILES_DIR}/hex_wetland.glb',
            TerrainType.MOUNTAIN: f'{settings.HEX_TILES_DIR}/hex_mountain.glb',
            TerrainType.DESERT: f'{settings.HEX_TILES_DIR}/hex_desert.glb',
            TerrainType.WATER: f'{settings.HEX_TILES_DIR}/hex_water.glb',
        }.get(terrain, f'{settings.HEX_TILES_DIR}/hex_grass.obj')

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

    @staticmethod
    def get_terrain_color(terrain):
        return {
            TerrainType.GRASSLAND: color.green,
            TerrainType.FOREST: rgb(0, 100, 0),
            TerrainType.WETLAND: color.blue,
            TerrainType.MOUNTAIN: color.gray,
            TerrainType.DESERT: color.yellow,
            TerrainType.WATER: color.cyan,
        }.get(terrain, color.green)
