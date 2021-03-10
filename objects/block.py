import pygame
import random
from objects.screen import Screen
from objects.ball import Ball
from objects.commons import Box
from objects.commons import COLOURS
from objects.ball import Ball


class Block(Box):

    def __init__(self, x: float, y: float, width: int, height: int, moving: bool, breakable: bool):
        colour = random.choice(COLOURS)
        super().__init__(x, y, width, height, colour)
        self.moving = moving
        self.breakable = breakable
        self.remove = False


def update(block: Block):
    pass


def check_collision(block: Block, ball: Ball):
    if block.rect.colliderect(ball.rect):
        block.remove = True
