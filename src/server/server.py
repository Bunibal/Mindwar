from ursina.networking import *

from src.common.util.util import register_functions
from src.server.game import Game
from src.server.rpc_functions.communication import COMMUNICATION_FUNCTIONS_TO_REGISTER
from src.server.rpc_functions.gameactions import GAMEACTIONS_FUNCTIONS_TO_REGISTER
from src.server.rpc_functions.lobby_rpc import LOBBY_FUNCTIONS_TO_REGISTER

peer = RPCPeer()


register_functions(peer, LOBBY_FUNCTIONS_TO_REGISTER)
register_functions(peer, COMMUNICATION_FUNCTIONS_TO_REGISTER)
register_functions(peer, GAMEACTIONS_FUNCTIONS_TO_REGISTER)

game = Game()

lobbies = []

peer.start("0.0.0.0", 8080, is_host=True)

if __name__ == '__main__':
    while True:
        peer.update()
        time.sleep(0.01)
# app.run()
