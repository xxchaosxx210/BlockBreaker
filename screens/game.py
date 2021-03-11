import pygame

from objects import (
    ball as _ball,
    paddle as _paddle,
    block as _block
)
from objects.commons import change_velocity
from objects.screen import Screen


def draw(screen: Screen, ball: _ball.Ball, paddle: _paddle.Paddle, blocks: list):
    screen.surface.fill(color=(0, 0, 0))
    pygame.draw.circle(screen.surface, ball.colour, (ball.rect.x, ball.rect.y), ball.radius)
    screen.surface.blit(paddle.surface, paddle.rect)
    for block in blocks:
        screen.surface.fill(rect=block.rect, color=block.colour)


def remove_dead_blocks(blocks: list):
    for block in reversed(blocks):
        if block.health <= 0:
            blocks.remove(block)


def loop(screen: Screen):
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    paddle = _paddle.Paddle(0, 0, 100, 20)
    ball = _ball.Ball(0, 0, 5)
    blocks = [_block.Block((screen.rect.width/2)-150, 50, 300, 40, False, True),
              _block.Block(10, 50, 50, 40, False, True)]
    _paddle.reset(paddle, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if not ball.moving:
                    _ball.start(ball, paddle)
                else:
                    ball.speed *= 2
                    ball.velocity = change_velocity(ball.velocity, ball.speed)
            elif event.type == pygame.KEYUP:
                _paddle.on_key_up(paddle, event.key)
            elif event.type == pygame.KEYDOWN:
                _paddle.on_key_down(paddle, event.key)
        # update
        _paddle.update(paddle, screen, dt)
        _ball.update(ball, paddle, screen, blocks, dt)
        for block in blocks:
            _block.update(block)
        # draw
        draw(screen, ball, paddle, blocks)
        if ball.fallen:
            _paddle.reset(paddle, screen)
            _ball.reset(ball)
            blocks = [_block.Block((screen.rect.width / 2) - 150, 50, 300, 40, False, True),
                      _block.Block(10, 50, 50, 40, False, True)]
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)

        # Remove any collided blocks
        remove_dead_blocks(blocks)