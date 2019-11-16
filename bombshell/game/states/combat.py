import time

from PIL import Image

from core.config import GlobalConfig
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.attributes import LastAbilityExecution
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.dead import DeadState
import game.states.grind
from game.states.loot import LootState
from game.states.policies.cast_failure import CastFailurePolicy
from game.states.pull import PullState
from game.target import Target
import game.states.loot


class CombatState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self._transition_to_grind = False
        self._previous_grind_state = previous_state
        self._next_state = None
        self._engaged_in_combat = False

    def interpret(self, character: Character, target: Target, screen: Image = None):
        if not character.is_in_combat and self._engaged_in_combat:
            self._next_state = LootState(self.controller, self.behavior, self.waypoints, self)
            return

        if not character.is_in_combat and not self._engaged_in_combat:
            self._next_state = game.states.grind.GrindState(self.controller, self.behavior, self.waypoints, self._previous_grind_state)
            return

        for action in self.behavior.interpret('grind', character, target):
            action.execute(self.controller)
            self._engaged_in_combat = True

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        return self._next_state


