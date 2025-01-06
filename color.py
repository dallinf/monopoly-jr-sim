from enum import Enum


class Color(Enum):
    BROWN = 1
    LIGHTBLUE = 2
    PINK = 3
    ORANGE = 4
    RED = 5
    YELLOW = 6
    GREEN = 7
    BLUE = 8
    WHITE = 9

    def __str__(self):
        return self.name.lower()
