from dataclasses import dataclass
from math import pi
from typing import Tuple, Dict, List

from core.logger import Logger
from core.util import load_from_file


@dataclass
class GrindPolicies:
    search_threshold: int = 5


@dataclass
class CombatMagicNumbers:
    wait_after_pull: int = 5
    targeting_frequency = 2


@dataclass
class MovementMagicNumbers:
    rad_per_turn: float = 0.0534
    turn_threshold: float = 0.2
    waypoint_difference_threshold = 0.01
    rad_per_sec: float = pi
    turn_on_search: Tuple[float, float] = (1, pi)


@dataclass
class KeyboardLayout:
    interact_with_target: str = 't'
    switch_target: str = 'tab'
    auto_move: str = '.'


@dataclass
class Config:
    behavior: dict
    waypoint: Dict[str, any]

    keyboard: KeyboardLayout = KeyboardLayout()

    movement: MovementMagicNumbers = MovementMagicNumbers()
    combat: CombatMagicNumbers = CombatMagicNumbers()
    grind_policy: GrindPolicies = GrindPolicies()

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


    @classmethod
    def load_from_data(cls, data: dict):
        for attr, value in data.items():
            setattr(cls.config, attr, value)
