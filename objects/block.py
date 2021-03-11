import pygame
from geometry.vector import Vector
from resources.spritesheet import SpriteSheet
import random

COLOUR_KEYS = ["red", "green"]


class Block:

    def __init__(self, x: float, y: float, moving: bool, breakable: bool, colour: str):
        self.rect = pygame.rect.Rect(x, y, 40, 40)
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.moving = moving
        self.breakable = breakable
        self.health = 3
        self.damage = 1
        self.colour = colour
        self.surface = SpriteSheet.block[self.colour].parse(0)
        self.offset = 0


def decrement_health(block: Block):
    block.health -= block.damage
    block.offset += 1
    block.surface = SpriteSheet.block[block.colour].parse(block.offset)


def generate_random_blocks():
    return list(map(lambda x: Block(x, 100, False, True, random.choice(COLOUR_KEYS)), range(40, 660, 40)))
