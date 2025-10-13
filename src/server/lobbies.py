class Lobbies:
    def __init__(self, rpc_peer):
        self.rpc_peer = rpc_peer
        # Register the methods with the rpc_peer
        self.register_rpcs()

    def register_rpcs(self):
        # Manually register methods as RPCs
        self.rpc_peer.rpc(self.update_player_position)
        self.rpc_peer.rpc(self.spawn_enemy)
        
    def update_player_position(self, connection, client_id, x, y, z):
        print(f"Player {client_id} moved to {x}, {y}, {z}")
        # Broadcast to other clients
        self.rpc_peer.send_rpc("update_player_position", client_id, x, y, z)

    def spawn_enemy(self, enemy_type, position):
        print(f"Spawning {enemy_type} at {position}")
        # Handle enemy spawning logic