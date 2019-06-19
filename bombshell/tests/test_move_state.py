import math
import unittest
from math import pi

from core.position import Position
from core.waypoint import PositionStorage
from game.states.move import MoveState


class FakeController:

    def __init__(self):
        self.val = 0

    def turn_right(self, val):
        self.val = val

    def turn_left(self, val):
        self.val = val


class FakeCharacter:

    def __init__(self):
        self.position = Position(0, 0)
        self.current_waypoint = 0


class TestMoveState(unittest.TestCase):

    def test_turn_left(self):
        fake_controller = FakeController()
        storage = PositionStorage()
        storage.parse([(0, 2)])
        move = MoveState(fake_controller, None, storage)
        fake_character = FakeCharacter()
        fake_character.position = Position(0, 0)

        move.interpret(fake_character, None)
        fake_character.position = Position(1, 1)
        move.interpret(fake_character, None)

        self.assertEqual(math.ceil(pi / 2 / move.RAD_PER_TURN), fake_controller.val)

