import pygame
from geometry.vector import Vector
from resources.spritesheet import SpriteSheet


class Block:

    """
    Red: 4 hits
    Pink: 3 hits
    orange: 2 hits
    green: 1 hit
    Blue: 1 hit
    """

    def __init__(self, x: float, y: float, colour: str, colour_offset: int,
                 moving: bool, breakable: bool, health: int):
        self.rect = pygame.rect.Rect(x, y, 40, 40)
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.moving = moving
        self.breakable = breakable
        self.health = health
        self.damage = 1
        self.surface = SpriteSheet.block[colour].parse(colour_offset)
        self.offset = 0
        self.colour = colour


def decrement_health(block: Block):
    if block.breakable:
        block.health -= block.damage
        block.offset += 1
        block.surface = SpriteSheet.block[block.colour].parse(block.offset)


def remove_dead_blocks(blocks: list):
    for block in reversed(blocks):
        if block.breakable and block.health <= 0:
            blocks.remove(block)
