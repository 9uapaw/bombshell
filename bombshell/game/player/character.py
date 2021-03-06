import enum
from typing import Tuple

from core.data import ExtractedData
from game.player.attributes import Resource, LastAbilityExecution, CastingState
from game.position.position import Position
from game.position.transform import normalize_facing


class Character:

    def __init__(self, resource_type: Resource = Resource.MANA):
        self.hp = 0
        self.resource = 0
        self.position = Position(0, 0)
        self.resource_type = resource_type
        self.is_moving = False
        self.is_in_combat = False
        self.current_waypoint = 0
        self.facing = 0
        self.casting = CastingState.IDLE
        self.last_ability = LastAbilityExecution.SUCCESS
        self.is_inventory_full = False
        self.has_pet = False
        self.first_class_resource = False
        self.pet_hp = 0
        self.pet_mana = 0

    def update(self, data: ExtractedData):
        self.hp = data.player_health
        self.resource = data.player_resource
        self.position = Position(data.player_position[0], data.player_position[1])
        self.is_in_combat = data.combat
        self.facing = normalize_facing(data.facing)
        self.last_ability = data.last_ability
        self.casting = data.casting
        self.is_inventory_full = data.is_inventory_full
        self.has_pet = data.player_has_pet
        self.first_class_resource = data.player_first_resource_available
        self.pet_hp = data.pet_health
        self.pet_mana = data.pet_mana

    def switch_moving(self):
        self.is_moving = not self.is_moving

    def __repr__(self):
        return "<HP: {}, Position: {}, Resource: {} {}>".format(self.hp, self.position, self.resource, self.resource_type.name)
