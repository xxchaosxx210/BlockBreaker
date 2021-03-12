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

    def __init__(self, x: float, y: float, moving: bool, breakable: bool,
                 colour: str, colour_offset: int = 0, border: bool = False):
        self.rect = pygame.rect.Rect(x, y, 40, 40)
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.moving = moving
        self.breakable = breakable
        self.border = border
        self.health = define_health(colour)
        self.damage = 1
        self.colour = colour
        self.surface = SpriteSheet.block[self.colour].parse(colour_offset)
        self.offset = 0


def define_health(colour: str):
    if colour == "red":
        return 3
    elif colour == "pink":
        return 3
    elif colour == "orange":
        return 2
    elif colour == "green":
        return 1
    elif colour == "blue":
        return 1
    else:
        return 1


def decrement_health(block: Block):
    if block.breakable:
        block.health -= block.damage
        block.offset += 1
        block.surface = SpriteSheet.block[block.colour].parse(block.offset)


def remove_dead_blocks(blocks: list):
    for block in reversed(blocks):
        if block.breakable and block.health <= 0:
            blocks.remove(block)
