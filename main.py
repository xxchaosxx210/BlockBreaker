import pygame

from objects import (
    paddle as _pad,
    ball as _ball,
    screen
)

from objects.commons import change_velocity


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    dt = 0.0

    scrn = screen.Screen(0, 0, 800, 600)
    paddle = _pad.Paddle(0, 0, 100, 20)
    ball = _ball.Ball(0, 0, 5)
    _pad.reset(paddle, scrn)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                if not ball.moving:
                    _ball.start(ball, paddle)
                else:
                    ball.velocity = change_velocity(ball, ball.speed*2)
            elif event.type == pygame.KEYUP:
                _pad.on_key_up(paddle, event.key)
            elif event.type == pygame.KEYDOWN:
                _pad.on_key_down(paddle, event.key)
        # update
        _pad.update(paddle, scrn, dt)
        _ball.update(ball, paddle, scrn, dt)
        # draw
        screen.draw(scrn)
        _pad.draw(paddle, scrn)
        _ball.draw(ball, scrn)
        if ball.fallen:
            _pad.reset(paddle, scrn)
            _ball.reset(ball)
        # flip
        pygame.display.flip()
        # count frames
        dt = 0.01 * clock.tick(scrn.frame_rate)


if __name__ == '__main__':
    main()