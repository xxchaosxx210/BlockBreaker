import pygame
import random
import math

from objects.block import (
    Block,
    define_colour
)
from geometry.vector import (
    Vector,
    random_vector,
    rotate
)


# triangle shape using a polygon
# fall over time
# turn as falling

MIN_BROKEN_PIECES = 5
MAX_BROKEN_PIECES = 10


def _generate_random_glass(block: Block):
    """
    creates a BrokenPiece and starts from the Centre of the broken Block
    Args:
        block:

    Returns:

    """
    c_x, c_y = block.rect.x + (block.rect.width / 2), block.rect.y + (block.rect.height / 2)
    return BrokenPiece(c_x, c_y, define_colour(block.colour))


def create_broken_glass(block: Block):
    """
    creates a list of BrokenPieces
    Args:
        block: block object to break

    Returns:
        list
    """
    broken_pieces = []
    for i in range(random.randint(MIN_BROKEN_PIECES, MAX_BROKEN_PIECES)):
        broken_pieces.append(_generate_random_glass(block))
    return broken_pieces


class BrokenPiece:

    def __init__(self, x: float, y: float, colour: tuple):
        self.colour = colour
        self.position = Vector(x, y)
        self.velocity = random_vector() * 2.1
        self.gravity = random.uniform(0.3, 2.1)
        self.fallen = False
        self.rotate_speed = random.uniform(1.2, 5.1)
        self.angle = 0
        self.rotate_scaler = random.randint(10, 30)

        self.pt2 = Vector(0, 0)
        self.pt3 = Vector(0, 0)

        self.define_shape(x, y)

    def define_shape(self, x, y):
        """
        Defines the shape of the triangle
        Args:
            x:
            y:

        Returns:

        """
        _min = 5
        _max = 20
        pt2 = Vector(random.randint(_min, _max), random.randint(_min, _max))
        pt3 = Vector(random.randint(_min, _max), random.randint(_min, _max))
        self.pt2 = random.choice((pt2, -pt2))
        self.pt3 = random.choice((pt3, -pt3))

    def update(self, dt: float):
        self.velocity.y += dt * self.gravity
        self.position += self.velocity + dt

    def check_bounds(self, game_rect: pygame.rect.Rect):
        if self.position.y > game_rect.bottom + 10:
            self.fallen = True

    def draw(self, buffer: pygame.Surface):
        pt2 = self.position + self.pt2
        pt3 = pt2 + self.pt3

        if self.angle >= 360:
            self.angle = 0

        # rotate
        pt2 = pt2 + rotate(self.angle) * self.rotate_scaler
        pt3 = pt3 + rotate(self.angle) * self.rotate_scaler

        self.angle += self.rotate_speed

        # create the triangle
        points = ((self.position.x, self.position.y),
                  (pt2.x, pt2.y),
                  (pt3.x, pt3.y))

        pygame.draw.polygon(buffer, self.colour, points)

