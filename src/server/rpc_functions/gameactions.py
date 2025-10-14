GAMEACTIONS_FUNCTIONS_TO_REGISTER = []

def rpcreg(f):
    GAMEACTIONS_FUNCTIONS_TO_REGISTER.append(f)
    return f

@rpcreg
def end_turn(connection, time_received):
    print(f"Player {connection.address} ended their turn")
    game.end_turn()
    # Notify others about new current player


@rpcreg
def move_unit(connection, time_received, unit_id: int, new_grid_position: tuple):
    print(f"Player {connection.address} moved unit {unit_id} to {new_grid_position}")
    # Find unit by id
    # Check if move is valid
    # Update unit position
    # Notify others

# ..... more game actions .....