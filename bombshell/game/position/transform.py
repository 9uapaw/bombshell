import math
from math import pi

from game.position.position import Position, Trajectory
from etc.const import RAD_PER_TURN


def calculate_trajectory(point: Position, facing: float) -> Trajectory:
    projected_x = point.point.x + 1 * math.cos(facing)
    projected_y = point.point.y + 1 * math.sin(facing)

    return Trajectory(point, Position(projected_x, projected_y), facing)


def normalize_facing(facing: float) -> float:
    if facing > 3 * pi / 2:
        normalized = facing - 3 * pi / 2
    else:
        normalized = pi / 2 + facing

    return normalized


def transform_turn(angle: float):
    return math.ceil(angle / RAD_PER_TURN)


