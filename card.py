from color import Color
from space import Space


class Card:
    def __init__(self, cost: int, collect_from_each_player: int, space: Space, color_1: Color, color_2: Color, is_get_out_of_timeout: bool, draw_another_card: bool):
        self.cost = cost
        self.collect_from_each_player = collect_from_each_player
        self.space = space
        self.color_1 = color_1
        self.color_2 = color_2
        self.is_get_out_of_timeout = is_get_out_of_timeout
        self.draw_another_card = draw_another_card

