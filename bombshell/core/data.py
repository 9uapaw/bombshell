import enum
from dataclasses import dataclass


class DistanceRange(enum.Enum):
    out_of_range = 0
    melee = 1
    cast = 2


@dataclass
class ExtractedData:
    player_health: float
    player_resource: float
    player_position: (float, float)
    target_health: float
    target_distance: DistanceRange
    combat: bool
