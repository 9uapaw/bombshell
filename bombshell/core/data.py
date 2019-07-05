import enum
from dataclasses import dataclass
from typing import Tuple


class DistanceRange(enum.Enum):
    unknown = -1
    out_of_range = 0
    melee = 1
    cast = 2


@dataclass
class ExtractedData:
    player_health: float
    player_resource: float
    player_position: Tuple[float, float]
    target_health: float
    target_distance: DistanceRange
    combat: bool
    facing: float
