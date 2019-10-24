import math
from math import pi
from typing import List

from core.config import GlobalConfig
from game.position.position import Position, Trajectory


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


def transform_turn(angle_difference: float):
    timespan = abs(angle_difference) / pi
    return timespan
    # return math.ceil(angle_difference / GlobalConfig.config.movement.rad_per_turn)


def find_closest_waypoint(waypoints: List[Position], position: Position) -> int:
    return waypoints.index(min(waypoints, key=position.calculate_distance_from))


def find_best_waypoint_route(routes: List[List[Position]], position: Position):
    best = (position.calculate_distance_from(routes[0][0]), 0)

    for i, route in enumerate(routes):
        distance = position.calculate_distance_from(route[0])

        if distance < best[0]:
            best = (distance, i)

    return best[1]

