from dataclasses import dataclass


@dataclass
class ExtractedData:
    player_health: int
    player_position: (float, float)
    target_health: int
    