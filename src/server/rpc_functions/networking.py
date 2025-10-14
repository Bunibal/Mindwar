NETWORKING_FUNCTIONS_TO_REGISTER = []
def rpcreg(f):
    NETWORKING_FUNCTIONS_TO_REGISTER.append(f)
    return f

@rpcreg
def on_connect(connection, time_received):
    print(f"New connection from {connection.address}")
    # Register Player and assign some UUID
    # Map UUID to IP address somehow
    # Notify others about new player
    # Check if disconnected before (if game running)
    # Send open lobbies

@rpcreg
def on_disconnect(connection, time_received):
    print(f"Connection lost from {connection.address}")
    # Notify others
    # Maybe pause? Remember ip address?

@rpcreg
def ragequit(connection, time_received, message: str):
    lobby.ragequit(connection, time_received, message)
    print(f"Player {connection.address} ragequit")
    # Notify others
    # Maybe pause? Remember ip address?
    # Have an LLM check whether the reason is legimate

