import enum

from core.data import ExtractedData
from core.position.position import Position


class Resource(enum.Enum):
    mana = 0
    energy = 1
    rage = 2


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

    def update(self, data: ExtractedData):
        self.hp = data.player_health
        self.resource = data.player_resource
        self.position = Position(data.player_position[0], data.player_position[1])
        self.is_in_combat = data.combat
        self.facing = data.facing

    def __repr__(self):
        return "<HP: {}, Position: {}, Resource: {} {}>".format(self.hp, self.position, self.resource, self.resource_type.name)
