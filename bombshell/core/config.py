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
    turn_threshold: float = 0.3
    waypoint_difference_threshold = 0.03
    rad_per_sec: float = pi
    turn_on_search: Tuple[float, float] = (1, pi)
    stuck_threshold = 0.1
    stop_threshold = 2.2

    stuck_last_n_position = 4
    stuck_turn_range = (0.2, 1.2)
    stuck_first_level_threshold = 3  # How many times does the first stuck level need to occur to trigger second level


@dataclass
class KeyboardLayout:
    interact_with_target: str = 't'
    switch_target: str = 'tab'
    auto_move: str = '.'


@dataclass
class CoreConfig:
    extract_error_threshold = 3
    recoverable_error_threshold = 3

    difference_between_two_waypoints = 1


@dataclass
class Config:
    behavior: dict
    waypoint: Dict[str, any]

    core: CoreConfig = CoreConfig()

    keyboard: KeyboardLayout = KeyboardLayout()

    movement: MovementMagicNumbers = MovementMagicNumbers()
    combat: CombatMagicNumbers = CombatMagicNumbers()
    grind_policy: GrindPolicies = GrindPolicies()

    roi: Tuple[int, int, int, int] = (0, 0, 500, 500)
    screen_res: Tuple[int, int, int, int] = (0, 45, 1650, 1050)


class GlobalConfig:
    """
    Used to represent the globally accessible constant values.
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
            Logger.warning("Unable to load global config: 'global.json'")

    @classmethod
    def load_from_data(cls, data: dict):
        for attr, value in data.items():
            setattr(cls.config, attr, value)
