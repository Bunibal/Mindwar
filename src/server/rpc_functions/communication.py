COMMUNICATION_FUNCTIONS_TO_REGISTER = []
def rpcreg(f):
    COMMUNICATION_FUNCTIONS_TO_REGISTER.append(f)
    return f

@rpcreg
def message(connection, time_received, msg: str):
    print(msg)
    # Send message to all other players