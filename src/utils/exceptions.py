class FactionException(Exception):
    def __init__(self, message="A Faction Error Occurred"):
        super().__init__(message)