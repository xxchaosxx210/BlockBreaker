import pygame

from geometry.vector import (
    Vector,
    approach
)

from objects.commons import (
    Box,
    change_velocity
)
from objects.screen import Screen

class Paddle(Box):

    def __init__(self, x, y, width, height, colour: tuple = (100, 255, 255)):
        super().__init__(x, y, width, height, colour)
        self.approach = Vector(0, 0)
        self.top_speed = 300


def update(paddle: Paddle, screen: Screen, dt: float):
    paddle.velocity.x = approach(paddle.approach.x, paddle.velocity.x, dt * 30)
    paddle.velocity.y = approach(paddle.approach.y, paddle.velocity.y, dt * 30)
    paddle.position = paddle.position + paddle.velocity * dt
    paddle.velocity = paddle.velocity + -4 * dt
    paddle.rect.x = paddle.position.x
    paddle.rect.y = paddle.position.y
    check_boundaries(paddle, screen)


def draw(paddle: Paddle, screen: Screen):
    screen.surface.fill(rect=paddle.rect, color=paddle.colour)


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


def reset(paddle: Paddle, screen: Screen):
    paddle.velocity = Vector(0, 0)
    x = (screen.rect.width/2) - (paddle.rect.width/2)
    y = (screen.rect.height-paddle.rect.height)
    paddle.position = Vector(x, y)
    paddle.approach = Vector(0, 0)


def check_boundaries(paddle: Paddle, screen: Screen):
    if paddle.rect.x < 0:
        paddle.rect.x = 0
        paddle.position.x = paddle.rect.x
        paddle.velocity.x *= -1
        paddle.velocity = change_velocity(paddle, 20)
    if paddle.rect.x > screen.rect.width-paddle.rect.width:
        paddle.rect.x = screen.rect.width-paddle.rect.width
        paddle.position.x = paddle.rect.x
        paddle.velocity.x *= -1
        paddle.velocity = change_velocity(paddle, 20)