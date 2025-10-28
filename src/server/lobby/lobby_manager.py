from src.server.lobby.lobby import Lobby, LobbyPlayer

from src.utils.logger import logger


class LobbyManager:

    def __init__(self):
        self.players = {}
        self.lobbies = {}

    def connect_player(self, connection):
        player = LobbyPlayer(connection)
        self.players[player.player_id] = player
        return player.player_id

    def disconnect_player(self, connection):
        player_id = next((pid for pid, p in self.players.items() if p.connection == connection), None)
        if player_id in self.players:
            player = self.players[player_id]
            if player.current_lobby:
                self.leave_lobby(player.current_lobby, player_id)
            del self.players[player_id]
        else:
            logger.warning(f"Player with id '{player_id}' does not exist.")
            raise ValueError(f"Player with id '{player_id}' does not exist.")

    def create_lobby(self, lobby_name, max_players):
        if any(lobby['lobby_name'] == lobby_name for lobby in self.lobbies.values()):
            logger.warning(f"Lobby with name '{lobby_name}' already exists.")
            raise ValueError(f"Lobby with name '{lobby_name}' already exists.")
        lobby = Lobby(lobby_name, max_players)
        self.lobbies[lobby.lobby_id] = lobby
        return lobby.lobby_id

    def join_lobby(self, lobby_id, player_id):
        if lobby_id in self.lobbies:
            lobby = self.lobbies[lobby_id]
            if len(lobby.players) < lobby.max_players:
                lobby.players.append(self.players[player_id])
            else:
                logger.info(f"Lobby '{lobby.lobby_name}' is full.")
                raise ValueError(f"Lobby '{lobby.lobby_name}' is full.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def leave_lobby(self, lobby_id, player_id):
        if lobby_id in self.lobbies:
            lobby = self.lobbies[lobby_id]
            if player_id in lobby.players:
                lobby.players.remove(self.players[player_id])
            else:
                logger.info(f"Player {player_id} is not in lobby.")
                raise ValueError(f"Player {player_id} is not in lobby.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def get_lobby_info(self, lobby_id, player_id):
        if lobby_id in self.lobbies:
            if player_id in self.lobbies[lobby_id].lobby_host:
                logger.debug(f"Player {player_id} started lobby with lobby id {lobby_id}.")
                return self.lobbies[lobby_id]
            else:
                logger.warning(f"Player {player_id} is not the host of lobby {lobby_id}.")
                raise ValueError("Only the lobby host can get lobby info.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def delete_lobby(self, lobby_id, player_id):
        if lobby_id in self.lobbies:
            if player_id == self.lobbies[lobby_id].lobby_host:
                del self.lobbies[lobby_id]
                logger.info(f"Lobby {lobby_id} deleted by host {player_id}.")
            else:
                logger.warning(f"Lobby {lobby_id} deletion attempted by player {player_id}.")
                raise ValueError("Only the lobby host can delete the lobby.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def change_lobby_settings(self, lobby_id, player_id, settings):
        pass

    def change_faction(self, lobby_id, player_id, faction):
        if lobby_id in self.lobbies:
            if player_id in self.lobbies[lobby_id].players:
                self.players[player_id].faction = faction
                logger.info(f"Player {player_id} changed faction to {faction} in lobby {lobby_id}.")
            else:
                logger.warning(f"Player {player_id} is not in lobby {lobby_id}.")
                raise ValueError(f"Player {player_id} is not in lobby {lobby_id}.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def set_lobby_status(self, lobby_id, status):
        if lobby_id in self.lobbies:
            self.lobbies[lobby_id].player_status = status
            logger.info(f"Lobby {lobby_id} status changed to {status}.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def set_player_status(self, player_id, status):
        if player_id in self.players:
            self.players[player_id].player_status = status
            logger.info(f"Player {player_id} status changed to {status}.")
            for lobby in self.lobbies.values():
                if player_id in [p.player_id for p in lobby.players]:
                    if all(p.player_status == "ready" for p in lobby.players):
                        lobby.player_status = "ready"
                        logger.info(f"Lobby {lobby.lobby_name} status changed to ready.")
                    break
        else:
            logger.warning(f"Player with id '{player_id}' does not exist.")
            raise ValueError(f"Player with id '{player_id}' does not exist.")
