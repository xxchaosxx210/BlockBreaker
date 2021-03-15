import pygame

from objects import (
    ball as _ball,
    paddle as _paddle,
    block as _block
)
from objects.commons import change_velocity
from objects.screen import Screen
import resources.tile as tile

BORDER = 40
BORDER_COLOUR = (112, 128, 144)


def draw(screen: Screen, ball: _ball.Ball, paddle: _paddle.Paddle, blocks: list):
    screen.surface.blit(screen.background, screen.rect)
    screen.surface.blit(ball.surface, ball.rect)
    screen.surface.blit(paddle.surface, paddle.rect)
    for block in blocks:
        screen.surface.blit(block.surface, block.rect)


def loop(screen: Screen):
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    game_rect = pygame.rect.Rect(screen.rect.x + BORDER, screen.rect.y + BORDER,
                                 screen.rect.right - BORDER, screen.rect.height)
    lives = 3
    level_mgr = tile.LevelManager()
    screen.background, blocks, paddle, ball = tile.load_first_level(level_mgr)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if not ball.moving:
                    _ball.start(ball)
                else:
                    ball.speed *= 1.2
                    ball.velocity = change_velocity(ball.velocity, ball.speed)
            elif event.type == pygame.KEYUP and event.key == pygame.K_2:
                for b in reversed(blocks):
                    if b.breakable:
                        blocks.remove(b)
            elif event.type == pygame.KEYUP:
                _paddle.on_key_up(paddle, event.key)
            elif event.type == pygame.KEYDOWN:
                _paddle.on_key_down(paddle, event.key)

        # update object positions check for collisions
        _paddle.update(paddle, game_rect, dt)
        _ball.update(ball, paddle, game_rect, blocks, dt)
        for block in blocks:
            if block.moving:
                _block.update(block, dt)

        # draw objects to screen
        draw(screen, ball, paddle, blocks)

        # check if ball has dropped off screen
        if ball.fallen:
            _paddle.reset(paddle)
            _ball.reset(ball)
            lives -= 1
            if lives < 0:
                running = False
        pygame.display.flip()

        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)

        # Remove any collided blocks
        _block.remove_dead_blocks(blocks)

        # Check if level complete
        if not list(filter(lambda b: b.breakable, blocks)):
            try:
                screen.background, blocks, paddle, ball = tile.load_next_level(level_mgr)
            except IndexError:
                # No more levels to load
                running = False
