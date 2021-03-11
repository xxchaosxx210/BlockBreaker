import pygame

from geometry.vector import (
    Vector,
    approach
)

from objects.commons import (
    Box,
    change_velocity
)

PADDLE_MIN_SPEED = 20


class Paddle(Box):

    def __init__(self, x, y, width, height, colour: tuple = (100, 255, 255)):
        super().__init__(x, y, width, height, colour)
        self.approach = Vector(0, 0)
        self.top_speed = 300
        self.drag = 30
        self.surface = pygame.image.load(".\\resources\\images\\paddle.png").convert_alpha()
        self.rect = self.surface.get_rect()


def update(paddle: Paddle, game_rect: pygame.rect.Rect, dt: float):
    paddle.velocity.x = approach(paddle.approach.x, paddle.velocity.x, dt * paddle.drag)
    paddle.velocity.y = approach(paddle.approach.y, paddle.velocity.y, dt * paddle.drag)
    paddle.position = paddle.position + paddle.velocity * dt
    paddle.velocity = paddle.velocity + -4 * dt
    paddle.rect.x = paddle.position.x
    paddle.rect.y = paddle.position.y
    check_boundaries(paddle, game_rect)


def on_key_down(paddle: Paddle, key: int):
    if key == pygame.K_LEFT:
        paddle.approach.x = -paddle.top_speed
    if key == pygame.K_RIGHT:
        paddle.approach.x = paddle.top_speed


def on_key_up(paddle: Paddle, key: int):
    if key == pygame.K_RIGHT:
        paddle.approach.x = 0
    if key == pygame.K_LEFT:
        paddle.approach.x = 0
    if key == pygame.K_1:
        paddle.drag = 90


def reset(paddle: Paddle, screen_rect: pygame.rect.Rect):
    paddle.velocity = Vector(0, 0)
    x = (screen_rect.width / 2) - (paddle.rect.width / 2)
    y = (screen_rect.height - paddle.rect.height)
    paddle.position = Vector(x, y)
    paddle.approach = Vector(0, 0)


def check_boundaries(paddle: Paddle, game_rect: pygame.rect.Rect):
    if paddle.rect.x < game_rect.x:
        paddle.rect.x = game_rect.x
        paddle.position.x = paddle.rect.x
        paddle.velocity.x *= -1
        paddle.velocity = change_velocity(paddle.velocity, PADDLE_MIN_SPEED)
    if paddle.rect.x > game_rect.width - paddle.rect.width:
        paddle.rect.x = game_rect.width - paddle.rect.width
        paddle.position.x = paddle.rect.x
        paddle.velocity.x *= -1
        paddle.velocity = change_velocity(paddle.velocity, PADDLE_MIN_SPEED)
