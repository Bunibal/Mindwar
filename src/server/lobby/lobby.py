import json
import random
import uuid
from enum import Enum

from src.entities.factions.base_faction import FactionType


class LobbyStatus(Enum):
    OPEN = "open"
    READY = "ready"
    IN_GAME = "in_game"
    CLOSED = "closed"


class PlayerStatus(Enum):
    NOT_READY = "not_ready"
    READY = "ready"
    NOT_INTERESTED = "not_interested"


class LobbyPlayer:
    def __init__(self, connection):
        self.player_id = str(uuid.uuid4())
        self.name = "random-" + str(random.randint(0, 9))
        self.connection = connection
        self.faction = FactionType.NONE
        self.player_status = PlayerStatus.NOT_READY

    def to_string(self):
        return """{
            "player_id": self.player_id,
            "faction": self.faction.value,
            "status": self.player_status.value,
        }"""


class Lobby:
    def __init__(self, player_id, lobby_name="Default Lobby", max_players=4):
        self.lobby_host = player_id
        self.lobby_status = LobbyStatus.OPEN
        self.lobby_id = str(uuid.uuid4())
        self.lobby_name = lobby_name
        self.max_players = max_players
        self.game_settings = {
            "map": "Default Map",
            "mode": "Standard",
            "turn_time": 60,
        }
        self.players = []

    def to_dict(self):
        return {
            "lobby_host": self.lobby_host,
            "status": self.lobby_status.value,
            "lobby_id": self.lobby_id,
            "lobby_name": self.lobby_name,
            "max_players": self.max_players,
            "game_settings": self.game_settings,
            "players": [player.to_string() for player in self.players],
        }


def serialize_obj(obj):
    if isinstance(obj, (Lobby, LobbyPlayer)):
        return obj.to_dict()
    raise TypeError("Type not serializable")


def to_json(obj):
    return json.dumps(serialize_obj(obj))
