from ursina import *

from src import settings
from src.entities.tiles.feature_type import FeatureType
from src.entities.tiles.terrain_type import TerrainType


class BaseTile(Button):
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
        self.street_entity = None
        self.street_rotation = None
        self.street_dirs = [(None, None), (None, None)]
        self.is_action_field = False

        model = self.get_model_for_terrain(self.terrain)
        position = self.hex_to_world(*self.grid_position)

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
        q, r = self.grid_position
        print(f"Clicked tile at row: {q}, col: {r}")
        print(f"Tile world position: {self.x}, {self.y}")
        print(f"Tile terrain: {self.terrain}")
        print(f"Tile feature: {self.feature}")
        if self.has_street:
            print(f"Tile has street: {self.street_entity}")
            print(f"Street rotation: {self.street_rotation}")
            print(f"Street directions: {self.street_dirs}")
            print(f"even: {self.grid_position[0] % 2 == 0}")

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

    def mark_as_action_field(self):
        if self.is_action_field:
            return  # already marked

        self.is_action_field = True

        self.action_field_highlight = Entity(
            parent=self,
            model='hex',  # same model shape
            color=color.rgba(255, 255, 0, 128),  # soft yellow glow
            scale=1,
            position=(0, 0.05, -0.2),  # slightly above the tile
            unlit=True
        )

    def clear_action_field(self):
        self.is_action_field = False
        if self.action_field_highlight:
            destroy(self.action_field_highlight)
            self.action_field_highlight = None

    def to_dict(self):
        return {
            "terrain": self.terrain.name,
            "feature": self.feature.name,
            "owner": self.owner.name if self.owner else None,
            "buildings": self.buildings if self.buildings else [],
            "units": self.units if self.units else [],
            "grid_position": self.grid_position,
            "has_street": self.has_street,
            "street_rotation": self.street_rotation,
            "street_dirs": self.street_dirs,
            "is_action_field": self.is_action_field,
            "street_entity": self.street_entity.model.name if self.street_entity else None,
        }

    def from_dict(self, data):
        data["terrain"] = TerrainType[data["terrain"]] if data.get("terrain") else None
        data["feature"] = FeatureType[data["feature"]] if data.get("feature") else None

        if self.is_action_field:
            self.is_action_field = False
            self.mark_as_action_field()

        if data.get("street_entity"):
            self.street_entity = Entity(
                model=data["street_entity"],
                parent=self,
                scale=1,
                position=(0, 0, -0.2),
                rotation_z=-self.street_rotation,
                unlit=True
            )
        else:
            self.street_entity = None
