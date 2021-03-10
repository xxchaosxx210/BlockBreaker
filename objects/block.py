import random
from objects.commons import Box
from objects.commons import COLOURS


class Block(Box):

    def __init__(self, x: float, y: float, width: int, height: int, moving: bool, breakable: bool):
        colour = random.choice(COLOURS)
        super().__init__(x, y, width, height, colour)
        self.moving = moving
        self.breakable = breakable
        self.health = 100


def update(block: Block):
    return
