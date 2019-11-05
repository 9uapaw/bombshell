import time

from PIL import Image

import game.states.grind
from core.config import GlobalConfig
from core.logger import Logger
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.combat import CombatState
from game.target import Target


class PullState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self._previous_grind_state = previous_state
        self._engaged = False
        self._last_pull = None
        self._transition_to_grind = False
        self._transition_to_combat = False

    def interpret(self, character: Character, target: Target, screen: Image = None):
        if self._engaged and self._last_pull and time.time() - self._last_pull > GlobalConfig.config.combat.wait_after_pull and not character.is_in_combat:
            self._engaged = False
            self._transition_to_grind = True
            return

        if not self._engaged:
            for action in self.behavior.interpret('pull', character, target):

                if character.is_moving:
                    self.controller.stop()
                    character.switch_moving()

                action._engaged = True
                self._last_pull = time.time()
                action.execute(self.controller)

        if character.is_in_combat:
            self._transition_to_combat = True

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        if self._transition_to_grind:
            return game.states.grind.GrindState(self.controller, self.behavior, self.waypoints, self._previous_grind_state)
        if self._transition_to_combat:
            return CombatState(self.controller, self.behavior, self.waypoints, self._previous_grind_state)
