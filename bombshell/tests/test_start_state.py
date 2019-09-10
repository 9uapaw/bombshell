import unittest

from game.position.position import Position, Direction
from game.position.waypoint import PositionStorage
from exception.core import PrerequisiteException
from game.states.start import StartState


class FakeController:

    def __init__(self):
        self.val = 0
        self.turn = None

    def turn_right(self, val):
        self.val = val
        self.turn = Direction.right

    def turn_left(self, val):
        self.val = val
        self.turn = Direction.left

    def move_forward(self):
        pass

    def stop(self):
        pass


class FakeCharacter:

    def __init__(self):
        self.position = Position(0, 0)
        self.current_waypoint = 0
        self.is_moving = False
        self.facing = 0


class TestStartState(unittest.TestCase):

    def setUp(self):
        self.storage = PositionStorage()
        self.controller = FakeController()
        self.start = StartState(self.controller, None, self.storage)

    def test_stop_on_transition_when_too_far_away(self):
        character = FakeCharacter()
        character.position = Position(50, 50)
        self.storage.parse([(20, 20)])

        with self.assertRaises(PrerequisiteException) as e:
            self.start.transition(character, None)

    def test_turn_left_to_waypoint(self):
        character = FakeCharacter()
        character.position = Position(50, 50)
        self.storage.parse([(20, 70)])

        self.start.interpret(character, None)

        self.assertEqual(Direction.left, self.controller.turn)

    def test_turn_right_to_waypoint(self):
        character = FakeCharacter()
        character.position = Position(50, 50)
        self.storage.parse([(92, 33)])

        self.start.interpret(character, None)

        self.assertEqual(Direction.right, self.controller.turn)

    def test_point(self):
        character = FakeCharacter()
        character.position = Position(530.0566, -432.1322)
        character.facing = 1.4452323
        self.storage.parse([(529.1963, -434.5789)])

        self.start.interpret(character, None)




