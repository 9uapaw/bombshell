from dataclasses import dataclass
from typing import Tuple


@dataclass
class Config:
    behavior: dict
    roi: Tuple[int, int, int, int] = (0, 0, 240, 360)
    screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)


class GlobalConfig:
    config = Config({})
