from enum import Enum, auto
from src.client.messages_from_server.lobbies import *

class MessageType(Enum):
    LOBBY_INFO = (lobby_info_received,)
    LOBBY_LIST = (send_lobby_list,)




