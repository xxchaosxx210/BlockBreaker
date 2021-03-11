import pygame

import screens.game as game

from objects.screen import Screen
import resources.font as font


BACKGROUND_COLOUR = (100, 0, 100)


def draw(screen: Screen):
    screen.surface.fill(color=BACKGROUND_COLOUR)


def draw_title(screen: Screen, f: font.Font):
    screen.surface.blit(f.surface, dest=(f.x, f.y))


def loop():
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    screen = Screen(0, 0, 800, 600)
    title = font.Font(10, 10, font.H1_FONT, (255, 255, 255), "BlockBreaker")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                game.loop(screen)
        # update
        # draw
        draw(screen)
        draw_title(screen, title)
        # flip
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)
