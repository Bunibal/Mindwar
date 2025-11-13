import os
from ursina.application import asset_folder

from utils.logger import logger

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parts = asset_folder.parts
if not parts[-1] == "client" or not parts[-2] == "src":
    logger.error(f"Ursina asset folder changed to {asset_folder}. Model paths may be incorrect.")

def full_path(relative_path):
    return "../../../" + relative_path
HEX_STREETS_DIR=full_path("assets/models/hex_streets")
HEX_TILES_DIR=full_path("assets/models/hex_tiles")
BUILDINGS_DIR=full_path("assets/models/buildings")
CARDS_DIR=full_path("assets/models/cards")
UNITS_DIR=full_path("assets/models/units")
CARDS=full_path("configs/cards.json")
FACTION_CONFIGS=full_path("configs/factions_config.json")
UI_ASSETS_DIR=full_path("assets/ui")

if __name__ == "__main__":
    print(HEX_TILES_DIR)

