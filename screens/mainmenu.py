import pygame

import screens.game as game
from objects import screen as _scrn


def loop():
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    screen = _scrn.Screen(0, 0, 800, 600)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                game.loop(screen)
        # update
        # draw
        _scrn.draw(screen)
        # flip
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)
