from core.data import ExtractedData
from game.behavior import CharacterBehavior
from game.character import Character, Resource
from game.control import CharacterController
from game.states.move import MoveState
from game.target import Target


class StateHandler:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior):
        self.character = Character(resource_type=Resource.mana)
        self.controller = controller
        self.behavior = behavior
        self.state = MoveState(self.controller, self.behavior)
        self.target = None

    def update(self, data: ExtractedData):
        if not data.combat and not self.character.is_moving:
            # self.controller.move_forward()
            self.character.is_moving = True

        self.character.hp = data.player_health
        if not self.target and data.target_health != 0:
            self.target = Target()
            self.target.hp = data.target_health
