from typing import Self

from color import Color


class Space:
    def __init__(self, name: str, cost: int, prev: Self, color: Color):
        self.name = name
        self.cost = cost
        self.owner = None
        self.next = None
        self.prev = prev
        self.color = color
        self.partner = None
        self.is_chance = False
        self.is_goto = False
        self.is_go = False
