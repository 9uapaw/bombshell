from dataclasses import dataclass
from math import pi
from typing import Tuple

from core.logger import Logger
from core.util import load_from_file


@dataclass
class MovementMagicNumbers:
    rad_per_turn: float = 0.0534
    turn_threshold: float = 0.2
    waypoint_difference_threshold = 0.01
    rad_per_sec: float = pi


@dataclass
class KeyboardLayout:
    interact_with_target: str = 't'
    switch_target: str = 'tab'
    auto_move: str = '.'


@dataclass
class Config:
    behavior: dict
    waypoint: dict
    keyboard: KeyboardLayout = KeyboardLayout()
    movement: MovementMagicNumbers = MovementMagicNumbers()
    roi: Tuple[int, int, int, int] = (0, 0, 240, 360)
    screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)


class GlobalConfig:
    """
    Used to represent the globally accessible magic constants.
    DO NOT ALTER THESE VALUES AFTER STARTING THREAD! IT IS A SINGLETON!
    """

    config = Config({}, {})

    @classmethod
    def load_from_file(cls, path: str):
        try:
            global_conf = load_from_file(path)
            cls.config.behavior = load_from_file(global_conf['behavior'])
            cls.config.waypoint = load_from_file(global_conf['waypoint'])
        except Exception as e:
            Logger.warning("Unable to load global config: 'global.json'", True)

