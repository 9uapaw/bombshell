import enum

from core.data import ExtractedData, DistanceRange


class TargetState(enum.Enum):
    idle = 0,
    in_combat = 1


class Target:

    def __init__(self):
        self.hp = 0
        self.state = TargetState.idle
        self.distance = DistanceRange.out_of_range

    def update(self, data: ExtractedData):
        self.hp = data.target_health
        self.distance = data.target_distance
