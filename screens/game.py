import pygame

from objects import (
    ball as _ball,
    screen as _scrn,
    paddle as _paddle
)
from objects.commons import change_velocity


def loop(screen: _scrn.Screen):
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
                    ball.velocity = change_velocity(ball, ball.speed * 2)
            elif event.type == pygame.KEYUP:
                _paddle.on_key_up(paddle, event.key)
            elif event.type == pygame.KEYDOWN:
                _paddle.on_key_down(paddle, event.key)
        # update
        _paddle.update(paddle, screen, dt)
        _ball.update(ball, paddle, screen, dt)
        # draw
        _scrn.draw(screen)
        _paddle.draw(paddle, screen)
        _ball.draw(ball, screen)
        if ball.fallen:
            _paddle.reset(paddle, screen)
            _ball.reset(ball)
        # flip
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(screen.frame_rate)