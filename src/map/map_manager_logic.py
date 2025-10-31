import itertools
import json
from math import sqrt
import random

import networkx as nx
from matplotlib import pyplot as plt

import settings
from entities.tiles.tile_logic_only import BaseTileLogic
from entities.tiles.feature_type import ACTION_FIELDS
from entities.tiles.feature_type import FLAT_TERRAINS
from entities.tiles.terrain_type import TerrainType

HEX_DIRECTIONS_EVEN = [(0, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
HEX_DIRECTIONS_ODD = [(0, 1), (-1, 1), (-1, 0), (0, -1), (1, 0), (1, 1)]


class MapManager:
    def __init__(self, rows=8, cols=6, n_action_fields=None, n_streets=None, terrain_weights=None):
        self.terrain_weights = terrain_weights
        if terrain_weights is not None:
            self.terrain_weights = self.normalize_weights(terrain_weights)
        self.n_action_fields = n_action_fields
        self.n_streets = n_streets
        self.action_fields = []
        self.street_network = None
        self.hex_graph = None
        self.rows = rows
        self.cols = cols
        self.tiles = []

    def generate_map(self):
        for q in range(self.rows):
            for r in range(self.cols):
                terrain = self.random_terrain(weights=self.terrain_weights)
                tile = BaseTileLogic(grid_position=(q, r), terrain=terrain)
                self.tiles.append(tile)
                if (q, r) in [(1, 1), (self.rows - 2, self.cols - 2), (self.rows - 2, 1), (1, self.cols - 2)]:
                    tile.mark_as_action_field()
                    self.action_fields.append(tile)
        self.build_hex_graph()
        self.action_fields = self.choose_random_action_fields((self.rows, self.cols))
        self.calculate_generate_street_network(n_edges=self.n_streets)
        self.clean_map_terrains()
        return self.tiles

    def clean_map_terrains(self):
        for tile in self.tiles:
            if tile.has_street:
                if tile.terrain not in FLAT_TERRAINS:
                    tile.terrain = self.random_terrain(flat=True, weights=self.terrain_weights)
            if tile.is_action_field:
                tile.terrain = random.choice(list(ACTION_FIELDS))
                
    def normalize_weights(self, raw_weights):
        total = sum(raw_weights.values())
        return {k: v / total for k, v in raw_weights.items()} if total else raw_weights

    def distance(self, tile1, tile2):
        x1, y1 = tile1.position
        x2, y2 = tile2.position
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def is_tile_close(self, tile1, tile2):
        if tile1 == tile2:
            return False
        return self.distance(tile1, tile2) < 9.5

    def choose_random_action_fields(self, size):
        if self.n_action_fields is None:
            n_fields = size[0] * size[1] // 20 - 2
        else:
            n_fields = self.n_action_fields - 4
        possible_fields = [tile for tile in self.tiles if tile.terrain in ACTION_FIELDS]
        action_fields = self.action_fields
        trys = 400
        while n_fields:
            too_close = False
            trys -= 1
            if trys == 0:
                break
            tile = random.choice(possible_fields)
            for action_tile in action_fields:
                if self.is_tile_close(tile, action_tile):
                    too_close = True
            if not too_close:
                action_fields.append(tile)
                tile.mark_as_action_field()
                possible_fields.remove(tile)
                n_fields -= 1
        return action_fields

    def angle_between_dirs(self, d1, d2, even):
        # Convert axial to angle in degrees (using simple approximation)
        def dir_to_angle(d, even):
            q, r = d
            if even:
                if (q, r) == (1, 0): return 0
                if (q, r) == (0, 1): return 60
                if (q, r) == (-1, 0): return 120
                if (q, r) == (-1, -1): return 180
                if (q, r) == (0, -1): return 240
                if (q, r) == (1, -1): return 300
            else:
                if (q, r) == (1, 1): return 0
                if (q, r) == (0, 1): return 60
                if (q, r) == (-1, 1): return 120
                if (q, r) == (-1, 0): return 180
                if (q, r) == (0, -1): return 240
                if (q, r) == (1, 0): return 300
            return False  # fallback

        return (dir_to_angle(d2, even) - dir_to_angle(d1, even)) % 360

    def determine_rotation(self, directions, even):
        dirs = list(directions)
        if len(dirs) != 2:
            return None, None  # Only handle 2-direction tiles for now

        d1, d2 = dirs
        angle = self.angle_between_dirs(d1, d2, even)
        angle = angle % 360

        if angle == 180:
            if even:
                # position in HEX_DIRECTIONS_EVEN
                rotation = HEX_DIRECTIONS_EVEN.index(d1) * 60
            else:
                # position in HEX_DIRECTIONS_ODD
                rotation = HEX_DIRECTIONS_ODD.index(d1) * 60
        elif angle in (120, 240):  # Wide curve
            if even and angle == 120:
                rotation = HEX_DIRECTIONS_EVEN.index(d1) * 60
            elif not even and angle == 120:
                rotation = HEX_DIRECTIONS_ODD.index(d1) * 60
            elif even and angle == 240:
                rotation = HEX_DIRECTIONS_EVEN.index(d2) * 60
            elif not even and angle == 240:
                rotation = HEX_DIRECTIONS_ODD.index(d2) * 60
        elif angle in (60, 300):  # Tight curve
            if even and angle == 60:
                rotation = HEX_DIRECTIONS_EVEN.index(d1) * 60
            elif not even and angle == 60:
                rotation = HEX_DIRECTIONS_ODD.index(d1) * 60
            elif even and angle == 300:
                rotation = HEX_DIRECTIONS_EVEN.index(d2) * 60
            elif not even and angle == 300:
                rotation = HEX_DIRECTIONS_ODD.index(d2) * 60
        else:
            rotation = None
        return rotation

    def random_terrain(self, flat=False, weights=None):
        if flat:
            terrain_types = list(FLAT_TERRAINS)
        else:
            terrain_types = list(TerrainType)[1:]  # skip TerrainType.NONE or 0-index type

        if weights:
            # Filter weights only for valid terrain types
            weight_list = [weights.get(t, 1) for t in terrain_types]
            return random.choices(terrain_types, weights=weight_list, k=1)[0]
        else:
            return random.choice(terrain_types)

    @classmethod
    def update(cls, action):
        pass

    def grid_distance(self, a, b):
        return self.distance(a, b)

    def calculate_generate_street_network(self, n_edges, spacing=3):
        self.street_graph = nx.Graph()
        tiles = range(len(self.action_fields))
        self.street_graph.add_nodes_from(tiles)

        # Step 1: Generate all candidate edges with spacing rule
        edge_candidates = []
        for a, b in itertools.combinations(tiles, 2):
            if self.grid_distance(self.action_fields[a], self.action_fields[b]) >= spacing:  # spacing rule
                real_dist = distance(self.action_fields[a].position, self.action_fields[b].position)
                edge_candidates.append((real_dist, a, b))

        edge_candidates.sort()  # shortest distance first

        added_edges = []

        for dist, a, b in edge_candidates:
            if len(added_edges) >= n_edges:
                break

            # Try adding the edge
            self.street_graph.add_edge(a, b)

            # Check planarity
            is_planar, _ = nx.check_planarity(self.street_graph)
            if not is_planar:
                self.street_graph.remove_edge(a, b)
            else:
                added_edges.append((a, b))

        tile_directions = self.determine_tile_directions_from_paths()

        for pos, directions in tile_directions.items():
            for tile in self.tiles:
                if tile.grid_position == pos:
                    tile.street_dirs = list(directions)
                    tile.has_street = True
                    model, rotation = self.determine_model_and_rotation(tile.street_dirs,
                                                                        tile.grid_position[0] % 2 == 0)
                    tile.street_rotation = rotation
                    tile.street_entity = Entity(
                        model=model,
                        parent=tile,
                        scale=1,
                        position=(0, 0, -0.2),
                        rotation_z=-rotation,
                        unlit=True
                    )
                    break

    def plot_street_graph(self, graph=None):
        if graph is None:
            # Use the existing graph if not provided
            G = self.street_graph
        else:
            G = graph

        # 1. Create position mapping from node index to 2D position
        if graph is None:
            pos = {i: (self.action_fields[i].position.x, self.action_fields[i].position.y) for i in G.nodes}
        else:
            pos = {i: (i[0], i[1]) for i in G.nodes}
        # 2. Plot
        plt.figure(figsize=(8, 8))
        nx.draw(G, pos,
                with_labels=True,
                node_color='lightblue',
                node_size=300,
                edge_color='gray',
                font_size=5,
                font_weight='bold')

        plt.title("Sanity Check: Street Graph")
        plt.axis("equal")
        plt.show()

    def build_hex_graph(self):  #
        G = nx.Graph()
        for tile in self.tiles:
            pos = tile.grid_position
            G.add_node(pos)
            if pos[0] % 2 == 0:
                HEX_DIRECTIONS = HEX_DIRECTIONS_EVEN
            else:
                HEX_DIRECTIONS = HEX_DIRECTIONS_ODD
            for dq, dr in HEX_DIRECTIONS:
                if (pos[0] + dq, pos[1] + dr) in G.nodes:
                    G.add_edge(pos, (pos[0] + dq, pos[1] + dr))
        return G

    def determine_tile_directions_from_paths(self):
        if not self.hex_graph:
            G = self.build_hex_graph()
        else:
            G = self.hex_graph
        tile_directions = {}  # Use dict because we skip reused tiles anyway
        used_paths = list()

        def subtract_pos(p1, p2):
            return (p1[0] - p2[0], p1[1] - p2[1])

        def calc_directions(a, b):
            start = self.action_fields[a].grid_position
            end = self.action_fields[b].grid_position

            # Copy the graph and exclude all other action fields
            G_current = G.copy()
            for tile in self.action_fields:
                gp = tile.grid_position
                if gp != start and gp != end and gp in G_current:
                    G_current.remove_node(gp)
            if (start, end) not in used_paths:
                try:
                    path = nx.shortest_path(G_current, source=start, target=end)
                except nx.NetworkXNoPath:
                    print(f"No path between {start} and {end}")
                    return
            else:
                return

            for i in range(1, len(path) - 1):  # Skip endpoints
                current = path[i]

                prev = path[i - 1]
                next = path[i + 1]

                dir1 = subtract_pos(prev, current)
                dir2 = subtract_pos(next, current)

                parity_even = current[0] % 2 == 0
                direction_set = HEX_DIRECTIONS_EVEN if parity_even else HEX_DIRECTIONS_ODD

                if dir1 in direction_set and dir2 in direction_set:
                    tile_directions[current] = [dir1, dir2]
                G.remove_node(current)  # Remove the node to avoid reusing it
            used_paths.append((start, end))
            used_paths.append((end, start))

        for a, b in self.street_graph.edges:
            if (a, b) not in used_paths and (b, a) not in used_paths:
                calc_directions(a, b)

        used_tiles = list(tile_directions.keys())  # already used tiles

        components = list(nx.connected_components(self.street_graph))
        print(f"Components: {len(components)}")

        if len(components) > 1:
            # connect two closest components without breaking planarity or using tile again
            while len(components) > 1:
                min_dist = float('inf')
                closest_pair = None
                for a in components[0]:
                    for b in components[1]:
                        if a in used_tiles or b in used_tiles:
                            continue
                        dist = self.grid_distance(self.action_fields[a], self.action_fields[b])
                        if dist < min_dist:
                            min_dist = dist
                            closest_pair = (a, b)

                if closest_pair:
                    a, b = closest_pair
                    self.street_graph.add_edge(a, b)
                    used_tiles.append(a)
                    used_tiles.append(b)
                    calc_directions(a, b)
                    components = list(nx.connected_components(self.street_graph))
                else:
                    break

        return tile_directions

    def plot_hex_paths(self, tile_directions):
        fig, ax = plt.subplots(figsize=(10, 10))

        # Plot all tiles as gray dots
        for tile in self.tiles:
            x, y = tile.position.x, tile.position.y
            ax.plot(x, y, 'o', color='lightgray', markersize=4)

        # Plot action_fields as blue
        for tile in self.action_fields:
            x, y = tile.position.x, tile.position.y
            ax.plot(x, y, 'o', color='blue', markersize=8)

        # Plot road tiles with direction arrows
        for grid_pos, directions in tile_directions.items():
            tile = next((t for t in self.tiles if t.grid_position == grid_pos), None)
            if not tile:
                continue
            x, y = tile.position.x, tile.position.y
            ax.plot(x, y, 's', color='orange', markersize=6)

            for dq, dr in directions:
                # Find neighbor in that direction
                neighbor_pos = (grid_pos[0] + dq, grid_pos[1] + dr)
                neighbor = next((t for t in self.tiles if t.grid_position == neighbor_pos), None)
                if neighbor:
                    nx, ny = neighbor.position.x, neighbor.position.y
                    ax.arrow(x, y, (nx - x) * 0.4, (ny - y) * 0.4,
                             head_width=0.2, length_includes_head=True, color='black', alpha=0.5)

        ax.set_aspect('equal')
        plt.title("Hex Tile Paths Through Road Graph")
        plt.show()

    def to_dict(self):
        return {
            'tiles': [tile.to_string() for tile in self.tiles],
            'action_fields': [tile.grid_position for tile in self.action_fields],
            'street_network': nx.to_dict_of_lists(self.street_graph),
            'rows': self.rows,
            'cols': self.cols,
        }

    def from_dict(self, data):
        self.tiles = []
        for tile_data in data['tiles']:
            tile = BaseTileLogic(**tile_data)
            tile.from_dict(tile_data)
            self.tiles.append(tile)
        self.action_fields = [self.get_tile_by_grid_position(pos) for pos in data['action_fields']]
        self.street_network = nx.from_dict_of_lists(data['street_network'])
        self.rows = data['rows']
        self.cols = data['cols']

    def save(self, filename='map_data.json'):
        data = self.to_dict()
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename='map_data.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.from_dict(data)

    def get_tile_by_grid_position(self, pos):
        for tile in self.tiles:
            if tile.grid_position == pos:
                return tile
        return None

    def get_random_action_fields(self, n):
        return random.choices(self.action_fields, n)
