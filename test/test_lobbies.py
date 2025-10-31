from client.ui.ui_manager import UIManager
from ursina.networking import RPCPeer


def test_create_and_join_lobby():
    peer = RPCPeer()
    ui_manager = UIManager(peer)
    peer.connect(ui_manager.server_ip, ui_manager.server_port)

    lobby_name = "Testlobby"
    max_players = 4

    lobby_id = peer.create_lobby(lobby_name, max_players)
    assert lobby_id is not None

    player_id = peer.connect_player(peer)
    assert player_id is not None

    peer.join_lobby(lobby_id, player_id)

    # Check if player is in lobby
    lobby = peer.get_lobby_info(lobby_id, player_id)
    assert lobby is not None
    assert player_id in lobby.players
