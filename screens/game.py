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
    pygame.draw.circle(screen.surface, ball.colour, (ball.rect.x, ball.rect.y), ball.radius)
    screen.surface.blit(paddle.surface, paddle.rect)
    for block in blocks:
        screen.surface.blit(block.surface, block.rect)


def loop(screen: Screen):
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    paddle = _paddle.Paddle(0, 0, 100, 20)
    ball = _ball.Ball(0, 0, 6)
    game_rect = pygame.rect.Rect(screen.rect.x + BORDER, screen.rect.y + BORDER,
                                 screen.rect.right - BORDER, screen.rect.height)
    blocks = []
    level_mgr = tile.LevelManager()
    tile.load_first_level(level_mgr)
    screen.background = tile.load_game_background(level_mgr)
    _paddle.reset(paddle, game_rect)
    lives = 3
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
        # update
        _paddle.update(paddle, game_rect, dt)
        _ball.update(ball, paddle, game_rect, blocks, dt)
        # draw
        draw(screen, ball, paddle, blocks)
        if ball.fallen:
            _paddle.reset(paddle, game_rect)
            _ball.reset(ball)
            lives -= 1
            if lives < 0:
                running = False
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)

        # Remove any collided blocks
        _block.remove_dead_blocks(blocks)

        # if not list(filter(lambda b: b.breakable, blocks)):
        #     _paddle.reset(paddle, game_rect)
        #     _ball.reset(ball)
