import enum


class Resource(enum.Enum):
    MANA = 0
    ENERGY = 1
    RAGE = 2


class LastAbilityExecution(enum.Enum):
    UNKNOWN = -1
    SUCCESS = 0
    OUT_OF_RANGE = 1
    OUT_OF_LOS = 2
    TOO_CLOSE = 3
    NOT_BEHIND = 4
    NOT_INFRONT = 5
    NO_TARGET = 6
