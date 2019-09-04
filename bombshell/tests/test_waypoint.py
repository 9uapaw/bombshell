import json
import math
import unittest
from math import pi, isclose

from sympy import Line

from core.data import ExtractedData, DistanceRange
from core.game_loop import GameLoop
from core.position.position import Position, Trajectory, Direction
from core.position.transform import calculate_trajectory, normalize_facing


class FakeScreen:

    def capture(self, *args):
        return range(0, 10)


class TestWaypoint(unittest.TestCase):

    def setUp(self):
        self.game_loop = GameLoop()
        self.game_loop.screen = FakeScreen()

    def test_record_waypoint(self):
        coords = iter(range(0, 10))

        def fake_points(*args):
            c = coords.__next__()

            return ExtractedData(0, 0, (c, c), 0, DistanceRange.out_of_range, False, 0)

        self.game_loop.extractor.extract_data_from_screen = fake_points

        self.game_loop.record_waypoints('../waypoints/test.json')
        with open('../waypoints/test.json') as test:
            self.assertEqual(10, len(json.load(test)['waypoints']))

    def test_calculate_trajectory(self):
        p1 = Position(2, -2)
        a1 = pi / 3
        a2 = 2 * pi / 3
        a3 = 4 * pi / 3
        a4 = 5 * pi / 3

        v1 = calculate_trajectory(p1, a1)
        v2 = calculate_trajectory(p1, a2)
        v3 = calculate_trajectory(p1, a3)
        v4 = calculate_trajectory(p1, a4)

        print(v1, v2, v3, v4)

    def test_calculate_angle(self):
        a = Position(2, -2)
        b = Position(1, -3)
        line = Trajectory(a, b)

        print(line)

    def test_normalize_facing(self):
        a1 = 1
        a2 = 6
        a3 = 2

        self.assertTrue(math.isclose(normalize_facing(a1), pi / 2 + a1))
        self.assertTrue(math.isclose(normalize_facing(a2), 2 * pi - a2))
        self.assertTrue(math.isclose(normalize_facing(a3), pi / 2 + a3))
