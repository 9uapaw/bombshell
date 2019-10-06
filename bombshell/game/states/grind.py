import time

from core.config import GlobalConfig
from core.logger import Logger
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.attributes import LastAbilityExecution
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.loot import LootState
from game.states.policies.cast_failure import CastFailurePolicy
from game.target import Target
import game.states.loot


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        Logger.debug("GRIND State")
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.engaged = False
        self.last_pull = None
        self._farming = False
        self._last_target_switch = time.time()
        self.looting_is_available = False
        self._cast_failure_policy = CastFailurePolicy(self.controller)

    def interpret(self, character: Character, target: Target):

        if target.hp > 0 and not self.engaged:
            for action in self.behavior.interpret('pull', character, target):

                if character.is_moving:
                    self.controller.stop()
                    character.switch_moving()

                self.engaged = True

                self.last_pull = time.time()
                action.execute(self.controller)

        if self._farming and not character.is_in_combat:
            self._farming = False
            self.looting_is_available = True

        if self.engaged and self.last_pull and time.time() - self.last_pull > GlobalConfig.config.combat.wait_after_pull and not character.is_in_combat:
            self.engaged = False

        if not character.is_in_combat and not self.engaged:
            for action in self.behavior.interpret('non_combat', character, target):
                action.execute(self.controller)
            self.waypoint_follower.move(character)
            if time.time() - self._last_target_switch > GlobalConfig.config.combat.targeting_frequency:
                self.controller.switch_target()
                self._last_target_switch = time.time()
        else:
            self._farming = True
            for action in self.behavior.interpret('grind', character, target):
                action.execute(self.controller)

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        if self.looting_is_available:
            return LootState(self.controller, self.behavior, self.waypoints)
