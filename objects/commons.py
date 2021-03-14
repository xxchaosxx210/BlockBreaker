from geometry.vector import (
    Vector,
    normalize
)

COLOURS = ((0,255,0), (255,0,0), (138,43,255))


def flip_colour(r: int, g: int, b: int):
    return (
        abs(r/1.4),
        abs(g/1.4),
        abs(b/1.4)
    )


def change_velocity(velocity: Vector, speed: int):
    return normalize(velocity) * speed


