import pygame
import random

from objects.block import (
    Block,
    define_colour
)
from geometry.vector import (
    Vector,
    random_vector
)


# triangle shape using a polygon
# fall over time
# turn as falling


def generate_random_glass(block: Block):
    c_x, c_y = block.rect.x + (block.rect.width / 2), block.rect.y + (block.rect.height / 2)
    return BrokenPiece(c_x, c_y, define_colour(block.colour))


class BrokenPiece:

    def __init__(self, x: float, y: float, colour: tuple):
        self.colour = colour
        self.position = Vector(x, y)
        self.velocity = random_vector() * 2.1
        self.gravity = 1
        self.fallen = False
        self.x2, self.y2 = (0, 0)
        self.x3, self.y3 = (0, 0)
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

        pt2 = random.choice((pt2, -pt2))
        pt3 = random.choice((pt3, -pt3))

        self.x2, self.y2 = (pt2.x, pt2.y)
        self.x3, self.y3 = (pt3.x, pt3.y)

    def update(self, dt: float):
        self.velocity.y += dt * self.gravity
        self.position += self.velocity + dt

    def check_bounds(self, game_rect: pygame.rect.Rect):
        if self.position.y > game_rect.bottom + 10:
            self.fallen = True

    def draw(self, buffer: pygame.Surface):
        x1, y1 = (self.position.x, self.position.y)
        x2, y2 = (self.position.x + self.x2, self.position.y + self.y2)
        x3, y3 = (x2 + self.x3, y2 + self.y3)
        pygame.draw.polygon(buffer, self.colour, ((x1, y1), (x2, y2), (x3, y3)))

