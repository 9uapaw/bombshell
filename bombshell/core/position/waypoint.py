from typing import List, Tuple

from core.data import ExtractedData
from core.position.position import Position


class PositionStorage:

    def __init__(self):
        self.waypoints = []  # type: List[Position]

    def add(self, waypoint: (float, float)):
        self.waypoints.append(Position(waypoint[0], waypoint[1]))

    def parse(self, points: List[Tuple[float, float]]):
        self.waypoints.extend([Position(x, y) for x, y in points])
