import json
import unittest
from unittest import mock

from core.data import ExtractedData, DistanceRange
from core.game_loop import GameLoop
from core.position import Position, Trajectory


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

            return ExtractedData(0, 0, (c, c), 0, DistanceRange.out_of_range, False)

        self.game_loop.extractor.extract_data_from_screen = fake_points

        self.game_loop.record_waypoints('../waypoints/test.json')
        with open('../waypoints/test.json') as test:
            self.assertEqual(10, len(json.load(test)['waypoints']))

    def test_calculate_angle(self):
        c1 = Position(1, 2)
        c2 = Position(2, 3)
        c3 = Position(3, 6)

        c5 = Position(0, 0)
        c6 = Position(2, -6)

        v1 = Trajectory(c1, c2)
        v2 = Trajectory(c1, c3)
        v3 = Trajectory(c5, c6)

        print(v1.angle, v2.angle, v3.angle, v3.end_point)

        print(v1.calculate_angle(v2))
