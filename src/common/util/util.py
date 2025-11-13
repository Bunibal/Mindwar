from ursina.networking import rpc
def register_functions(rpc_peer, functions):
    for f in functions:
        #rpc_peer.register_function(f)
        rpc(rpc_peer)(f)