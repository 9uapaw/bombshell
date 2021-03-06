import enum
import math

from sympy import Point, Line, Ellipse, Circle


class Direction(enum.Enum):
    left = 0
    right = 1


class Position:

    def __init__(self, x: float, y: float):
        self.point = Point(x, y)
        self.x = x
        self.y = y

    def is_close_to(self, other: 'Position', threshold: float):
        x_diff = self.point.x * threshold if self.point.x else threshold
        y_diff = self.point.y * threshold if self.point.y else threshold
        x_point = self.point.x + x_diff
        y_point = self.point.y + y_diff
        new_pos = Position(x_point, y_point)

        radius = self.calculate_distance_from(new_pos)

        area = Circle(self.point, radius)

        return area.encloses_point(other.point)

    def calculate_distance_from(self, other: 'Position') -> float:
        return math.sqrt((self.point.x - other.point.x)**2 + (self.point.y - other.point.y)**2)

    def __eq__(self, other: 'Position'):
        return other.point.x == self.point.x and other.point.y == self.point.y

    def __repr__(self):
        return "<{}, {}>".format(self.point.x.evalf(), self.point.y.evalf())


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
        angle = self.calculate_angle_between(other)
        direction = self.calculate_direction(other)

        if angle > math.pi:
            angle = 2 * math.pi - angle
            direction = Direction.right if direction == Direction.left else Direction.left

        return angle, direction

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
                angle = 2 * math.pi - angle

        return angle

    def __repr__(self):
        return "<{}, {}>".format(self.start_point, self.end_point)
