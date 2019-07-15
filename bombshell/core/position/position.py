import enum
import math

from sympy import Point, Line, Ellipse
from sympy.vector import Vector, Point as VectorPoint
from mpmath import degree, radians


class Direction(enum.Enum):
    left = 0
    right = 1


class Position:

    def __init__(self, x: float, y: float):
        self.point = Point(x, y)

    def is_close_to(self, other: 'Position', threshold: float):
        hradius = self.point.x * threshold if self.point.x else threshold
        vradius = self.point.y * threshold if self.point.y else threshold
        area = Ellipse(self.point, hradius, vradius)

        return area.encloses_point(other.point)

    def calculate_distance_from(self, other: 'Position'):
        return math.sqrt((self.point.x - other.point.x)**2 + (self.point.y - other.point.y)**2)

    def __eq__(self, other: 'Position'):
        return other.point.x == self.point.x and other.point.y == self.point.y

    def __repr__(self):
        return self.point.__repr__()


class Trajectory:

    def __init__(self, a: Position, b: Position, angle: float=-1):
        self.vector = Line(a.point, b.point)
        self.angle = angle if angle != -1 else self._calculate_angle(self.vector)

    @property
    def start_point(self):
        x, y = self.vector.p1.evalf()
        return x, y

    @property
    def end_point(self):
        x, y = self.vector.p2.evalf()
        return x, y

    def calculate_turn(self, other: 'Trajectory'):
        return self.calculate_angle_between(other), self.calculate_direction(other)

    def calculate_angle_between(self, other: 'Trajectory') -> float:
        return abs(self.angle - other.angle)

    def calculate_direction(self, other: 'Trajectory') -> Direction:
        return Direction.left if self.angle <= other.angle else Direction.right

    @staticmethod
    def _calculate_angle(line: Line) -> float:
        angle = line.angle_between(Line((0, 0), (1, 0))).evalf()
        if line.p2.x <= line.p1.x:
            if line.p2.y <= line.p1.y:
                angle = math.pi - angle + math.pi
        else:
            if line.p2.y <= line.p1.y:
                angle = 3 * math.pi / 2 + angle

        return angle

    def __repr__(self):
        return self.vector.__repr__()


