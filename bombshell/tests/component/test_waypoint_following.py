import threading
import unittest
from math import sin, cos, pi
from typing import Tuple

from PIL import Image

from core.data import ExtractedData, DistanceRange
from core.game_loop import GameLoop
from etc.const import RAD_PER_TURN
from game.control.control import CharacterController

RUN_SPEED = 1


class FakeScreen:

    def __init__(self, screen_size: (int, int, int, int)):
        self.screen_size = (0, 40, 800, 640)
        self.capturing = True

    def capture(self):
        pass

    def stop_capturing(self):
        self.capturing = False


class FakeImageExtractor:

    def __init__(self):
        self.position = (0, 0)
        self.facing = 0

        self.lock = threading.Lock()
        self.facing_lock = threading.Lock()

    def extract_data_from_screen(self, screen: Image) -> ExtractedData or None:
        return ExtractedData(0, 0, self.read_position(), 0, DistanceRange.out_of_range, True, self.read_facing())

    def change_position(self, by_value: Tuple[float, float]):
        with self.lock:
            self.position = by_value

    def read_position(self):
        with self.lock:
            return self.position

    def change_facing(self, by_value: float):
        with self.facing_lock:
            self.facing = by_value

    def read_facing(self):
        with self.facing_lock:
            return self.facing


class FakeController(CharacterController):

    extractor = None # type: FakeImageExtractor
    stopped = False

    def move_forward(self):
        def _calculate_movement():
            while not self.stopped:
                pos = self.extractor.read_position()
                facing = self.extractor.read_facing()
                new_pos = (pos[0] + RUN_SPEED * sin(facing), pos[1] + RUN_SPEED * cos(facing))
                print('new pos', new_pos)
                self.extractor.change_position(new_pos)

        thr = threading.Thread(target=_calculate_movement)
        thr.start()

    def stop(self):
        self.stopped = True

    def cast_spell(self, key: int):
        pass

    def turn_left(self, key_presses: int):
        facing = self.extractor.read_facing()
        facing_diff = RAD_PER_TURN * key_presses

        if facing + facing_diff > 2 * pi:
            new_facing = facing_diff - (2 * pi - facing)
        else:
            new_facing = facing + facing_diff

        self.extractor.change_facing(new_facing)

    def turn_right(self, key_presses: int):
        facing = self.extractor.read_facing()
        facing_diff = RAD_PER_TURN * key_presses

        if facing - facing_diff < 0:
            new_facing = 2 * pi - (facing_diff - facing)
        else:
            new_facing = facing - facing_diff

        self.extractor.change_facing(new_facing)


class TestWaypointFollowing(unittest.TestCase):

    def setUp(self):
        self.position = (0, 0)
        self.game_loop = GameLoop()
        self.extractor = FakeImageExtractor()
        self.game_loop.extractor = self.extractor
        self.controller = FakeController()
        self.controller.extractor = self.extractor
        self.game_loop.state.controller = self.controller

    def test_go(self):
        self.controller.move_forward()
        print(self.extractor.read_position())
        self.controller.turn_left(3)
        print(self.extractor.read_position())
        self.controller.turn_left(5)
        print(self.extractor.read_position())
        self.controller.turn_right(9)
        print(self.extractor.read_position())
        self.controller.turn_right(7)
        print(self.extractor.read_position())
        self.controller.stop()

