from typing import Self
from board import Board
from card import Card
from chance import Chance
from space import Space
from color import Color

class Player:
    def __init__(self, id: int, starting_cash: int, starting_space: Space):
        self.id = id
        self.space = starting_space
        self.cash = starting_cash
        self.owned_spaces = []
        self.has_get_out_of_timeout = False
        self.chance_cards = []
        if id == 0:
            self.color = Color.RED
        elif id == 1:
            self.color = Color.BLUE
        elif id == 2:
            self.color = Color.GREEN
        elif id == 3:
            self.color = Color.YELLOW

    def move(self, board: Board, roll: int, players: list[Self], chance: Chance) -> Space:
        original_space = self.space
        self.space = board.get_space(self.space, roll)

        passed_go_log = ""
        if board.passed_go(original_space, self.space):
            self.gain_cash(2)
            passed_go_log = "passed Go"

        log = self.handle_space(board, players, chance)

        return f"Player {self.id} {self.color} rolled a {roll} and {log}, {passed_go_log}. Has ${self.cash} remaining."

    def handle_space(self, board: Board, players: list[Self], chance: Chance, free: bool = False) -> str:
        if self.space.is_go:
            # self.gain_cash(2) Gained it elsewhere
            return f"landed on Go and gained $2"
        elif self.space.is_goto:
            self.space = board.timeout_corner
            if self.has_get_out_of_timeout:
                self.has_get_out_of_timeout = False
                return f"landed on Goto Timeout and moved to {self.space.name}. Used Get Out of Timeout card"
            else:
                self.spend_cash(1)
                return f"landed on Goto Timeout and moved to {self.space.name}. Paid $1"
        elif self.space.is_chance:
            log = self._handle_chance(board, players, chance)
            return f"landed on Chance and drew a card. {log}"
        elif self.space.cost > 0 and self.space.owner is None:
            log = ""
            if not free:
                self.spend_cash(self.space.cost)
                log = f"paid {self.space.cost}"
            else:
                log = "got it for free"

            self.space.owner = self.id
            self.owned_spaces.append(self.space)
            return f"landed on {self.space.name} and {log}"
        elif self.space.cost > 0 and self.space.owner != self.id:
            log = self._handle_other_player_space(players)
            return f"landed on {self.space.name} {log}"
        elif self.space.cost > 0 and self.space.owner == self.id:
            # We own this space
            return f"landed on {self.space.name} and already owns it"
        elif self.space.name == "Free Parking" or self.space.name == "Just Visiting":
            return f"landed on {self.space.name}"
        else:
            raise Exception(f"Unknown space: {self.space.name}")

    def spend_cash(self, amount: int):
        self.cash -= amount

    def gain_cash(self, amount: int):
        self.cash += amount

    def gain_chance(self, card: Card):
        self.chance_cards.append(card)

    def _handle_chance(self, board: Board, players: list[Self], chance: Chance) -> str:
        card = chance.draw()

        if card.is_get_out_of_timeout:
            self.has_get_out_of_timeout = True
            return f"It was a Get Out of Timeout card"
        elif card.draw_another_card:
            next_player = self._find_next_player(players)
            next_player.gain_chance(card)
            other_log = self._handle_chance(board, players, chance)
            return f"It was a Draw Another Card chance card and gave it to Player {next_player.id}. {other_log}"
        elif card.collect_from_each_player > 0:
            for player in players:
                player.spend_cash(card.collect_from_each_player)
            
            self.gain_cash(card.collect_from_each_player)
            # Do it twice for laziness, because it just got subtracted
            self.gain_cash(card.collect_from_each_player)
            return f"It was a Collect From Each Player chance card and collected {card.collect_from_each_player} from each player"
        elif card.cost > 0:
            self.gain_cash(card.cost)
            return f"It was a Gain Cash chance card and gained {card.cost}"
        elif card.cost < 0:
            self.spend_cash(card.cost)
            return f"It was a Spend Cash chance card and spent {card.cost}"
        elif card.space is not None:
            original_space = self.space
            self.space = card.space
            passed_go_log = ""
        
            if self.space.is_go:
                self.gain_cash(2)
                passed_go_log = "passed Go"
            elif board.passed_go(original_space, self.space):
                self.gain_cash(2)
                passed_go_log = "passed Go"

            other_log = self.handle_space(board, players, chance, free=True)
            return f"It was a Move To Space chance card and {other_log}, {passed_go_log}"
        else:
            other_log = self._handle_color_chance(board, card, players)
            return f"It was a Color Chance card {card.color_1} and {card.color_2}. {other_log}"

    def _handle_color_chance(self, board: Board, card: Card, players: list[Self]) -> str:
        # Find all spaces of both colors
        spaces = [space for space in board.spaces if space.color == card.color_1 or space.color == card.color_2]

        # Find the highest unowned rent space of those colors. Ties go to the first space found.
        highest_rent = max(spaces, key=lambda s: s.cost if s.owner is None else 0).cost
        all_highest_rent_spaces = [space for space in spaces if space.cost == highest_rent and space.owner is None]

        # Move to that space
        if len(all_highest_rent_spaces) > 0:
            distances = []
            for space in all_highest_rent_spaces:
                distances.append(board.find_space_distance(self.space, space))

            self.space = all_highest_rent_spaces[distances.index(min(distances))]
            self.space.owner = self.id
            self.owned_spaces.append(self.space)
            return f"moved to {self.space.name}. Got it for free"

        # If no spaces are found, find the space owned by this player and move to it. Ties go to the last space found.
        owned_spaces = [space for space in spaces if space.owner == self.id]
        if len(owned_spaces) > 0:
            distances = []
            for space in owned_spaces:
                distances.append(board.find_space_distance(self.space, space))

            self.space = owned_spaces[distances.index(max(distances))]
            return f"moved to {self.space.name}. Owns it already"
        
        # If still no spaces are found, find the space with the lowest rent and move to it. Ties go to the last space found.
        lowest_rent = min(spaces, key=lambda s: s.cost if s.owner is None else float('inf')).cost
        all_lowest_rent_spaces = [space for space in spaces if space.cost == lowest_rent]
        
        if len(all_lowest_rent_spaces) > 0:
            distances = []
            for space in all_lowest_rent_spaces:
                distances.append(board.find_space_distance(self.space, space))

            self.space = all_lowest_rent_spaces[distances.index(max(distances))]
            other_log = self._handle_other_player_space(players)
            return f"moved to {self.space.name}. Paid {self.space.cost} to the owner. {other_log}"

        raise Exception("No space found for color chance")

    def _handle_other_player_space(self, players: list[Self]) -> str:
        # Landed on another player's space
        other_player = next((p for p in players if p.id == self.space.owner), None)

        if self.space.partner.owner == self.space.owner:
            other_player.gain_cash(self.space.cost * 2)
            self.spend_cash(self.space.cost * 2)
            return f"has a monopoly and paid {self.space.cost * 2} to the owner"
        else:
            self.spend_cash(self.space.cost)
            other_player.gain_cash(self.space.cost)
            return f"paid {self.space.cost} to the owner"
    def _find_next_player(self, players: list[Self]) -> Self:
        current_index = players.index(self)
        next_index = (current_index + 1) % len(players)
        return players[next_index]
