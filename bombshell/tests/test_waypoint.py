import json
import unittest
from math import pi, isclose
from unittest import mock

from core.data import ExtractedData, DistanceRange
from core.game_loop import GameLoop
from core.position import Position, Trajectory, Direction
from core.waypoint import PositionStorage
from game.states.move import MoveState


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
        p1 = Position(0, 0)
        p2 = Position(1, 1)
        p3 = Position(1, 2)
        p4 = Position(2, 1)

        v1 = Trajectory(p1, p2)
        v2 = Trajectory(p2, p3)
        v3 = Trajectory(p2, p4)

        self.assertTrue(isclose(pi/4, v1.calculate_angle(v2)))
        self.assertEqual(Direction.left, v1.calculate_direction(v2))
        self.assertTrue(isclose(pi/4, v1.calculate_angle(v3)))
        self.assertEqual(Direction.right, v1.calculate_direction(v3))
