from geometry.vector import (
    Vector,
    normalize
)
import pygame


class Box:

    def __init__(self, x: float, y: int, width: int, height, colour: tuple=(255, 255, 255)):
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.colour = colour


class Circle:
    
    def __init__(self, x: float, y: float, radius: int, colour: tuple = (255, 255, 255)):
        self.radius = radius
        self.diameter = self.radius * 2
        self.rect = pygame.rect.Rect(x, y, self.diameter, self.diameter)
        self.velocity = Vector(0, 0)
        self.position = Vector(x, y)
        self.colour = colour


def change_velocity(obj: object, speed: int):
    obj.speed = speed
    return (normalize(obj.velocity) * speed)


