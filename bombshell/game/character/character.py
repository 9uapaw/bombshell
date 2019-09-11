import enum

from core.data import ExtractedData
from game.position.position import Position
from game.position.transform import normalize_facing


class Resource(enum.Enum):
    MANA = 0
    ENERGY = 1
    RAGE = 2


class LastAbilityExecution(enum.Enum):
    SUCCESS = 0
    OUT_OF_RANGE = 1
    OUT_OF_LOS = 2
    TOO_CLOSE = 3
    NOT_BEHIND = 4
    NOT_INFRONT = 5
    NO_TARGET = 6


class Character:

    def __init__(self, resource_type: Resource):
        self.hp = 0
        self.resource = 0
        self.position = Position(0, 0)
        self.resource_type = resource_type
        self.is_moving = False
        self.is_in_combat = False
        self.current_waypoint = 0
        self.facing = 0
        self.last_ability = LastAbilityExecution.SUCCESS

    def update(self, data: ExtractedData):
        self.hp = data.player_health
        self.resource = data.player_resource
        self.position = Position(data.player_position[0], data.player_position[1])
        self.is_in_combat = data.combat
        self.facing = normalize_facing(data.facing)
        self.last_ability = data.last_ability

    def switch_moving(self):
        self.is_moving = not self.is_moving

    def __repr__(self):
        return "<HP: {}, Position: {}, Resource: {} {}>".format(self.hp, self.position, self.resource, self.resource_type.name)
