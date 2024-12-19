import random
from board import Board
from card import Card
from color import Color


class Chance:
    def __init__(self, board: Board):
        self.board = board
        self.setup_deck(board)

    def draw(self) -> Card:
        if len(self.cards) == 0:
            self.setup_deck(self.board)
        return self.cards.pop(0)
    
    def setup_deck(self, board: Board):
        self.cards = [
            Card(0, 0, None, Color.PINK, Color.BLUE, False, False),
            Card(0, 0, None, Color.LIGHT_BLUE, None, False, False),
            Card(0, 0, None, Color.BLUE, None, False, False),
            Card(0, 0, None, Color.GREEN, None, False, False),
            Card(0, 0, None, Color.LIGHT_BLUE, Color.RED, False, False),
            Card(0, 0, None, Color.RED, None, False, False),
            Card(0, 0, None, Color.ORANGE, Color.GREEN, False, False),
            Card(0, 0, None, Color.ORANGE, None, False, False),
            Card(0, 0, None, Color.GREEN, None, False, False),
            Card(0, 0, None, Color.BROWN, Color.YELLOW, False, False),
            Card(0, 0, None, None, None, False, True),
            Card(0, 0, None, None, None, False, True),
            Card(0, 0, None, None, None, False, True),
            Card(0, 0, board.go_space, None, None, False, False),
            Card(0, 0, board.go_space, None, None, False, False),
            Card(0, 0, board.beach, None, None, False, False),
            Card(0, 0, board.amusement_park, None, None, False, False),
            Card(-2, 0, None, None, None, False, False),
            Card(2, 0, None, None, None, False, False),
            Card(0, 1, None, None, None, False, False),
            Card(0, 0, None, None, None, True, False),
        ]
        random.shuffle(self.cards)