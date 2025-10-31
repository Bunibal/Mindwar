from enum import Enum, auto
from client.messages_from_server.lobby_handling import *

class MessageType(Enum):
    LOBBY_INFO = (lobby_info_received,) # Yes we need a singleton tuple here every time
    LOBBY_LIST = (send_lobby_list,) # Enum works very strange when the value is a function
    GAME_STARTED = (game_started,)
    ERROR = ()
    TEXT_MESSAGE = ()