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
    pet_health: int
    pet_mana: int
    target_health: int
    target_distance: DistanceRange
    combat: bool
    facing: float
    casting: CastingState
    target_id: int
    target_guid: int
    last_ability: LastAbilityExecution
    is_inventory_full: bool
    player_has_pet: bool
    player_first_resource_available: bool
    target_in_combat: bool

