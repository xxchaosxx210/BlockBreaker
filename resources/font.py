import pygame.freetype
import pygame
import os

pygame.freetype.init()

FONT_PATH = os.path.join(os.getcwd(), r"resources\ARCADE.TTF")

H1_FONT = pygame.freetype.Font(FONT_PATH, 48)
H2_FONT = pygame.freetype.Font(FONT_PATH, 32)
H3_FONT = pygame.freetype.Font(FONT_PATH, 24)
H4_FONT = pygame.freetype.Font(FONT_PATH, 20)
H5_FONT = pygame.freetype.Font(FONT_PATH, 16)


class Font:

    def __init__(self, x: float, y: float,
                 font: pygame.freetype.Font,
                 fg_colour: tuple, text: str):
        self.surface, self.rect = font.render(text, fgcolor=fg_colour)
        self.x = x
        self.y = y

