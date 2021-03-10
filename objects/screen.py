import pygame


class Screen:

    def __init__(self, x: int, y: int, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height))
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.frame_rate = 144
