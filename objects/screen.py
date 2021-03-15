import pygame


class Screen:

    def __init__(self, x: int, y: int, width: int, height: int, background_image: pygame.Surface = None):
        self.surface = pygame.display.set_mode((width, height))
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.frame_rate = 144
        self.background = background_image
