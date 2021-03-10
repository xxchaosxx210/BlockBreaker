import pygame

from objects import (
    ball as _ball,
    paddle as _paddle
)
from objects.commons import change_velocity
from objects.screen import Screen


def draw(screen: Screen, ball: _ball.Ball, paddle: _paddle.Paddle):
    screen.surface.fill(color=(0, 0, 0))
    pygame.draw.circle(screen.surface, ball.colour, (ball.rect.x, ball.rect.y), ball.radius)
    screen.surface.fill(rect=paddle.rect, color=paddle.colour)


def loop(screen: Screen):
    clock = pygame.time.Clock()
    running = True
    dt = 0.0
    paddle = _paddle.Paddle(0, 0, 100, 20)
    ball = _ball.Ball(0, 0, 5)
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
        _ball.update(ball, paddle, screen, dt)
        # draw
        draw(screen, ball, paddle)
        if ball.fallen:
            _paddle.reset(paddle, screen)
            _ball.reset(ball)
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)