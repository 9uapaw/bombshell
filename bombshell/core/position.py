import enum

from sympy import Point, Line, Ellipse
from mpmath import degree, radians


class Direction(enum.Enum):
    left = 0
    right = 1


class Position:

    def __init__(self, x: float, y: float):
        self.point = Point(x, y)

    def is_close_to(self, other: 'Position', threshold: float):
        hradius = self.point.x * threshold
        vradius = self.point.y * threshold
        area = Ellipse(self.point, hradius, vradius)

        return area.encloses_point(other.point)

    def __eq__(self, other: 'Position'):
        return other.point.x == self.point.x and other.point.y == self.point.y

    def __repr__(self):
        return self.point.__repr__()


class Trajectory:

    def __init__(self, a: Position, b: Position):
        self.vector = Line(a.point, b.point)

    @property
    def angle(self):
        return self.vector.angle_between(Line((0, 0), (1, 0))).evalf()

    @property
    def end_point(self):
        x, y = self.vector.p2.evalf()
        return x, y

    def calculate_angle(self, other: 'Trajectory'):
        return self.vector.angle_between(other.vector).evalf()

    def calculate_direction(self, other: 'Trajectory'):
        a, b, c = self.vector.coefficients
        y = (-a * other.end_point[0] - c) / b

        if y >= other.end_point[1]:
            return Direction.right
        else:
            return Direction.left


