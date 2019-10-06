import enum
from dataclasses import dataclass
from typing import Tuple
from game.player.attributes import LastAbilityExecution, CastingState


class DistanceRange(enum.IntEnum):
    unknown = -1
    out_of_range = 0
    melee = 1
    cast = 2


@dataclass
class ExtractedData:
    player_health: int
    player_resource: int
    player_position: Tuple[float, float]
    target_health: int
    target_distance: DistanceRange
    combat: bool
    facing: float
    casting: CastingState
    target_id: int
    target_guid: int
    last_ability: LastAbilityExecution

