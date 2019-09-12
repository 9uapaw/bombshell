import enum

from core.data import ExtractedData
from game.player.attributes import Resource, LastAbilityExecution
from game.position.position import Position
from game.position.transform import normalize_facing


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
