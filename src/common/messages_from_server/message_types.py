from enum import Enum, auto
from src.client.messages_from_server.lobbies import *

class MessageType(Enum):
    LOBBY_INFO = lobby_info_received

def flag(message_type: MessageType):
    def decorator(func):
        FLAGGED_FUNCTIONS[message_type] = func
        return func
    return decorator


