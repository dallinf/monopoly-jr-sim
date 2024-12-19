from player import Player


class WinResult:
    def __init__(self, player_id: int, num_turns: int, players: list[Player], game_log: list[str]):
        self.player_id = player_id
        self.num_turns = num_turns
        self.players = players
        self.game_log = game_log
