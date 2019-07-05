import math
from math import pi, sin, tan
from typing import Tuple

from core.position.position import Position, Trajectory, Direction
from etc.const import RAD_PER_TURN


def calculate_turn(current: Tuple[Position, Position], follow_up:Tuple[Position, Position]):
    char_trajectory = Trajectory(*current)
    waypoint_trajectory = Trajectory(*follow_up)

    angle = char_trajectory.calculate_angle(waypoint_trajectory)
    direction = char_trajectory.calculate_direction(waypoint_trajectory)

    return angle, direction


def calculate_turn_from_trajectory(current: Trajectory, follow_up: Trajectory):
    angle = current.calculate_angle(follow_up)
    direction = current.calculate_direction(follow_up)

    return angle, direction


def calculate_trajectory(point: Position, facing: float) -> Trajectory:
    sample_y_length = 1
    normalized_angle = facing
    x_sign = -1
    y_sign = 1

    if pi / 2 < facing < pi:
        y_sign = -1
        normalized_angle = pi - facing
    elif pi < facing < 3 * pi / 2:
        y_sign = -1
        x_sign = 1
        normalized_angle = facing - pi
    elif 3 * pi / 2 < facing < 2 * pi:
        x_sign = 1
        normalized_angle = 2 * pi - facing

    bc = round(tan(normalized_angle) * sample_y_length, 6)
    projected_x = point.point.x + x_sign * bc
    projected_y = point.point.y + y_sign * sample_y_length

    return Trajectory(point, Position(projected_x, projected_y))


def normalize_facing(facing: float) -> float:
    if facing > 3 * pi / 2:
        normalized = 2 * pi - facing
    else:
        normalized = pi / 2 + facing

    return normalized


def transform_turn(angle: float):
    return math.ceil(angle / RAD_PER_TURN)


