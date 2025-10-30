from src.server.lobby.lobby import Lobby, LobbyPlayer

from src.utils.logger import logger


class LobbyManager:
    def __init__(self):
        self.players = {}
        self.lobbies = {}

    def connect_player(self, connection):
        player = LobbyPlayer(connection)
        self.players[player.player_id] = player
        return player

    def _get_player_from_connection(self, connection):
        try:
            return next(p for pid, p in self.players.items() if p.connection == connection)
        except StopIteration:
            logger.warning("No player found with the given connection")
            raise ValueError("No player found with the given connection")

    def _get_lobby_from_player(self, player_or_id):
        """Get the lobby_id for a player if they are in a lobby.

        Args:
            player_or_id: Either a LobbyPlayer object or a player_id string

        Returns:
            lobby_id if player is in a lobby, None otherwise
        """
        # Handle both player object and player_id
        if isinstance(player_or_id, LobbyPlayer):
            player_id = player_or_id.player_id
        else:
            player_id = player_or_id

        # Search through all lobbies for this player
        for lobby_id, lobby in self.lobbies.items():
            if any(p.player_id == player_id for p in lobby.players):
                return lobby

        return None

    def disconnect_player(self, connection):
        player = self._get_player_from_connection(connection)
        # if player.current_lobby:
        self.leave_lobby(player)
        del self.players[player.id]
        # else:
        # logger.warning(f"Player with id '{player.id}' does not exist.")
        # raise ValueError(f"Player with id '{player.id}' does not exist.")

    def set_player_name(self, connection, player_name):
        player = self._get_player_from_connection(connection)
        player.name = player_name

    def create_lobby(self, connection, lobby_name, max_players):
        player = self._get_player_from_connection(connection)
        logger.info("Player %s created lobby %s with player count %d", player.name, lobby_name, max_players)
        if any(lobby.lobby_name == lobby_name for lobby in self.lobbies.values()):
            logger.warning(f"Lobby with name '{lobby_name}' already exists.")
            raise ValueError(f"Lobby with name '{lobby_name}' already exists.")
        lobby = Lobby(player.player_id, lobby_name, max_players)
        self.lobbies[lobby.lobby_id] = lobby
        return lobby.lobby_id

    def join_lobby(self, connection, lobby_id):
        player = self._get_player_from_connection(connection)
        if lobby_id in self.lobbies:
            lobby = self.lobbies[lobby_id]
            if len(lobby.players) < lobby.max_players:
                lobby.players.append(player)
                return lobby
            else:
                logger.info(f"Lobby '{lobby.lobby_name}' is full.")
                raise ValueError(f"Lobby '{lobby.lobby_name}' is full.")
        else:
            logger.warning(f"Lobby with id '{lobby_id}' does not exist.")
            raise ValueError(f"Lobby with id '{lobby_id}' does not exist.")

    def leave_lobby(self, player_id):
        lobby = self._get_lobby_from_player(player_id)
        lobby.players.remove(self.players[player_id])

    def get_lobby_info(self, connection, lobby_id):
        player = self._get_player_from_connection(connection)
        if lobby_id in self.lobbies:
            if player.player_id in self.lobbies[lobby_id].lobby_host:
                logger.debug(f"Player {player.player_id} started lobby with lobby id {lobby_id}.")
                return self.lobbies[lobby_id]
            else:
                logger.warning(f"Player {player.player_id} is not the host of lobby {lobby_id}.")
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
