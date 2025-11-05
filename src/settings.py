import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# HEX_STREETS_DIR="../assets/models/hex_streets"
# HEX_TILES_DIR="../assets/models/hex_tiles"
# BUILDINGS_DIR="../assets/models/buildings"
# CARDS_DIR="../assets/models/cards"
# UNITS_DIR="../assets/models/units"
# CARDS="../../configs/cards.json"
# FACTION_CONFIGS="configs/factions_config.json"
HEX_STREETS_DIR=os.path.join(parent_dir, "assets/models/hex_streets")
HEX_TILES_DIR=os.path.join(parent_dir, "assets\\models\\hex_tiles")
BUILDINGS_DIR=os.path.join(parent_dir, "assets/models/buildings")
CARDS_DIR=os.path.join(parent_dir, "assets/models/cards")
UNITS_DIR=os.path.join(parent_dir, "assets/models/units")
CARDS=os.path.join(parent_dir, "configs/cards.json")
FACTION_CONFIGS=os.path.join(parent_dir, "configs/factions_config.json")