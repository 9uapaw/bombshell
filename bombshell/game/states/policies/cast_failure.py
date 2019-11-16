import random

from core.config import GlobalConfig
from game.control.control import CharacterController
from game.player.attributes import LastAbilityExecution
from game.player.character import Character
from game.position.position import Direction
from game.target import Target


class CastFailurePolicy:

    def __init__(self, controller: CharacterController):
        self.controller = controller
        self._rolled_direction = Direction(random.randint(0, 1))
        self._turns = 0

    def interpret(self, character: Character, target: Target):
        if character.last_ability == LastAbilityExecution.SUCCESS:
            self._turns = 0
        elif character.last_ability == LastAbilityExecution.NOT_INFRONT:
            if self._turns >= GlobalConfig.config.grind_policy.search_threshold:
                self.controller.turn(self._rolled_direction, random.randrange(*GlobalConfig.config.movement.turn_on_search))
                self._turns += 1
