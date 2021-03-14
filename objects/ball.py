import random
import math
import pygame

from geometry.vector import (
    Vector,
    normalize,
    copy
)

from objects.paddle import Paddle
from objects.block import Block
from objects.block import decrement_health


class Ball:

    def __init__(self, x, y, fallen, moving, speed):
        self.surface = pygame.image.load(r".\/resources\/images\/ball.png").convert_alpha()
        self.radius = self.surface.get_width() / 2
        self.diameter = self.surface.get_width()
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = Vector(0, 0)
        self.position = Vector(x, y)
        self.moving = moving
        self.fallen = fallen
        self.DEFAULT_POSITION = copy(self.position)
        self.DEFAULT_SPEED = speed
        self.speed = speed


def reset(ball: Ball):
    ball.moving = False
    ball.fallen = False
    ball.speed = ball.DEFAULT_SPEED
    ball.velocity = Vector(0, 0)
    ball.position = copy(ball.DEFAULT_POSITION)


def attach_to_paddle(ball: Ball, paddle: Paddle):
    ball_center = (paddle.rect.width / 2) - ball.radius
    x = paddle.position.x + ball_center
    y = ball.DEFAULT_POSITION.y
    ball.position = Vector(x, y)
    ball.rect.x = ball.position.x
    ball.rect.y = ball.position.y


def update(ball: Ball, paddle: Paddle, game_rect: pygame.rect.Rect, blocks: list, dt: float):
    if ball.moving:
        ball.position = ball.position + ball.velocity * dt
    else:
        attach_to_paddle(ball, paddle)
    ball.rect.x = ball.position.x
    ball.rect.y = ball.position.y
    # check if paddle has hit ball
    if not been_hit(ball, paddle):
        check_boundaries(ball, game_rect)
        if ball.fallen:
            return
        # check if ball has hit a block
        for block in blocks:
            if hit_block(ball, block):
                break


def hit_block(ball: Ball, block: Block):
    if block.rect.colliderect(ball.rect):
        collision_threshold = 10
        # Ball hit top of block. Ignore collision if ball is heading in other direction
        block_top_hit = abs(ball.rect.bottom - block.rect.top)
        if block_top_hit < collision_threshold and ball.velocity.y > 0:
            ball.velocity.y = -ball.velocity.y
            decrement_health(block)
            return True
        # Ball hit bottom of block
        block_bottom_hit = abs(ball.rect.top - block.rect.bottom)
        if block_bottom_hit < collision_threshold and ball.velocity.y < 0:
            ball.velocity.y = -ball.velocity.y
            decrement_health(block)
            return True
        # Ball hit left of Block
        block_left_hit = abs(ball.rect.right - block.rect.left)
        if block_left_hit < collision_threshold and ball.velocity.x > 0:
            ball.velocity.x = -ball.velocity.x
            decrement_health(block)
            return True
        # Ball hit right of block
        block_right_hit = abs(ball.rect.left - block.rect.right)
        if block_right_hit < collision_threshold and ball.velocity.x < 0:
            ball.velocity.x = -ball.velocity.x
            decrement_health(block)
            return True
    return False


def been_hit(ball: Ball, paddle: Paddle):
    """check to see if ball hit paddle

    Args:
        ball (Ball): Ball object
        paddle (Paddle): Paddle Object

    Returns:
        [bool]: returns True if Ball benn hit
    """
    collision_threshold = 15
    if ball.rect.colliderect(paddle.rect) and ball.velocity.y > 0.0:
        ontop = abs(ball.rect.bottom - paddle.rect.top)
        if ontop < collision_threshold:
            ball.velocity.y = -ball.velocity.y
        else:
            ball.velocity.x = -ball.velocity.x
        return True
    return False


def check_boundaries(ball: Ball, game_rect: pygame.rect.Rect):
    """make sure the ball bounces off the walls and falls if hit the floor

    Args:
        game_rect: game rect object
        ball: Ball object
    """
    threshold = 5
    if ball.rect.left < game_rect.x + threshold and ball.velocity.x < 0.0:
        ball.velocity.x = -ball.velocity.x
    if ball.rect.right > game_rect.width - threshold and ball.velocity.x > 0.0:
        ball.velocity.x = -ball.velocity.x
    if ball.rect.top < game_rect.y + threshold and ball.velocity.y < 0.0:
        ball.velocity.y = -ball.velocity.y
    if ball.rect.top > game_rect.height + 100:
        ball.fallen = True


def new_angled_velocity():
    angles = [float(x) for x in range(120, 150, 1)]
    angles.extend([float(x) for x in range(30, 50, 1)])
    angle = random.choice(angles)
    x = math.cos(math.radians(angle))
    y = math.sin(math.radians(angle))
    return normalize(Vector(x, y))


def start(ball: Ball):
    direction = new_angled_velocity()
    ball.velocity = ball.velocity + direction * ball.speed
    ball.moving = True
    ball.fallen = False
