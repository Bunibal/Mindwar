from enum import Enum


class GameEventType(Enum):
    MOVE_UNIT = "move_unit"
    ATTACK_UNIT = "attack_unit"