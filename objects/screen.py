import pygame


class Screen:

    def __init__(self, x: int, y: int, width: int, height: int, colour: tuple=(0, 0, 0)):
        self.surface = pygame.display.set_mode((width, height))
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.colour = colour
        self.frame_rate = 144


def draw(screen: Screen):
    screen.surface.fill(screen.colour)