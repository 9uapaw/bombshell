import time

from PIL import Image

import game.states.grind
from core.config import GlobalConfig
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.combat import CombatState
from game.states.policies.cast_failure import CastFailurePolicy
from game.target import Target


class PullState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self._previous_grind_state = previous_state
        self._engaged = False
        self._last_pull = time.time()
        self._next_state = None
        self._cast_failure = CastFailurePolicy(self.controller)

    def interpret(self, character: Character, target: Target, screen: Image = None):
        if time.time() - self._last_pull > GlobalConfig.config.combat.wait_after_pull and not character.is_in_combat:
            Logger.info("Pull was unsuccessful, transitioning back to GrindState")
            self._next_state = game.states.grind.GrindState(self.controller, self.behavior, self.waypoints, self._previous_grind_state)
            return

        self._cast_failure.interpret(character, target)

        for action in self.behavior.interpret('pull', character, target):
            self._last_pull = time.time()
            if character.is_moving:
                self.controller.stop()
                character.switch_moving()

            action.execute(self.controller)

        if character.is_in_combat:
            self._next_state = CombatState(self.controller, self.behavior, self.waypoints, self._previous_grind_state)

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        return self._next_state
