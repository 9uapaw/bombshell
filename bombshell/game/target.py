import enum


class TargetState(enum.Enum):
    idle = 0,
    in_combat = 1


class Target:

    def __init__(self):
        self.hp = 0
        self.state = TargetState.idle

    