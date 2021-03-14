import pygame
from geometry.vector import (
    Vector,
    normalize
)

from resources.spritesheet import SpriteSheet


class Block:

    def __init__(self, x: float, y: float, _id: int, colour: str, colour_offset: int,
                 moving: bool, breakable: bool, health: int, end_x: int, end_y: int, speed: int):
        self.rect = pygame.rect.Rect(x, y, 40, 40)
        self.moving = moving
        self.breakable = breakable
        self.health = health
        self.damage = 1
        self.surface = SpriteSheet.block[colour].parse(colour_offset)
        self.offset = 0
        self.colour = colour
        self.id = _id
        if moving:
            self.speed = speed
            self.position = Vector(x, y)
            direction = Vector(end_x, end_y) - self.position
            self.velocity = normalize(direction) * self.speed
            self.START_X = x
            self.START_Y = y
            self.END_X = end_x
            self.END_Y = end_y


def decrement_health(block: Block):
    if block.breakable:
        block.health -= block.damage
        block.offset += 1
        block.surface = SpriteSheet.block[block.colour].parse(block.offset)


def remove_dead_blocks(blocks: list):
    for block in reversed(blocks):
        if block.breakable and block.health <= 0:
            blocks.remove(block)


def update(block: Block, dt: float):
    block.position = block.position + block.velocity * dt
    block.rect.x = block.position.x
    block.rect.y = block.position.y
    check_bounds(block)


def check_bounds(block: Block):
    threshold = 5
    # gone too far right?
    if block.position.x > block.END_X + threshold:
        block.velocity.x = -block.velocity.x
    # gone too far left?
    elif block.position.x < block.START_X - threshold:
        block.velocity.x = -block.velocity.x


