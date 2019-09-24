from dataclasses import dataclass
from typing import Tuple


@dataclass
class MovementMagicNumbers:
    rad_per_turn: float = 0.0534
    turn_threshold: float = 0.1
    waypoint_difference_threshold = 0.01


@dataclass
class KeyboardLayout:
    interact_with_target: str = 't'
    switch_target: str = 'tab'
    auto_move: str = '.'


@dataclass
class Config:
    behavior: dict
    keyboard: KeyboardLayout = KeyboardLayout()
    movement: MovementMagicNumbers = MovementMagicNumbers()
    roi: Tuple[int, int, int, int] = (0, 0, 240, 360)
    screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)


class GlobalConfig:
    """
    Used to represent the globally accessible magic constants.
    DO NOT ALTER THESE VALUES AFTER STARTING THREAD! IT IS A SINGLETON!
    """

    config = Config({})
