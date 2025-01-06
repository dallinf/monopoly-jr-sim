import random

from board import Board
from card import Card
from chance import Chance
from color import Color
from player import Player
from win_result import WinResult

class Game:
    def __init__(self, num_players: int):
        self.board = Board()
        match num_players:
            case 2:
                starting_cash = 20
            case 3:
                starting_cash = 18
            case _:
                starting_cash = 16
        self.players = [Player(i, starting_cash, self.board.go_space) for i in range(num_players)]
        self.chance = Chance(self.board)
        self.game_log = []
        self.current_player = self.players[0]

    def simulate_next_player(self) -> str:
        if self.is_game_over():
            return f"Game over because a player is bankrupt"

        result = self.take_turn(self.current_player)
        self.game_log.append(result)
        self.current_player = self.players[(self.players.index(self.current_player) + 1) % len(self.players)]
        return result

    def simulate(self, step_by_step=False) -> WinResult:
        turn_count = 0
        game_over = False
        while not game_over and turn_count < 1000:
            for player in self.players:
                if self.is_game_over():
                    game_over = True
                    self.game_log.append(f"Game over because a player is bankrupt")
                    break

                self.game_log.append(self.take_turn(player))
            
            turn_count += 1

            if step_by_step:
                break

        if turn_count >= 1000:
            return WinResult(None, turn_count, self.players, self.game_log)

        return WinResult(max(self.players, key=lambda p: p.cash).id, turn_count, self.players, self.game_log)

    def is_game_over(self) -> bool:
        return any(player.cash < 0 for player in self.players)

    def take_turn(self, player: Player):
        log = None
        if len(player.chance_cards) > 0:
            player.chance_cards.pop(0)
            next_unowned_property = self.board.find_max_unowned_property(player.space)
            if next_unowned_property is not None:
                player.space = next_unowned_property
                player.spend_cash(next_unowned_property.cost)
                next_unowned_property.owner = player.id
                player.owned_spaces.append(next_unowned_property)
                return f"Player {player.id} used chance to land on {next_unowned_property.name} and bought it for {next_unowned_property.cost}"
            else:
                player.gain_cash(2)
                log = f"Player {player.id} used chance to move and gained $2. Then took a turn."

        roll = random.randint(1, 6)
        other_log = player.move(self.board, roll, self.players, self.chance)
        if log is None:
            log = other_log
        else:
            log = f"{log}. {other_log}"
        return log
