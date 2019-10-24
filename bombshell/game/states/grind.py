import time

from PIL import Image

from core.config import GlobalConfig
from core.logger import Logger
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.attributes import LastAbilityExecution
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.combat import CombatState
from game.states.dead import DeadState
from game.states.loot import LootState
from game.states.policies.cast_failure import CastFailurePolicy
from game.states.pull import PullState
from game.target import Target
import game.states.loot


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        Logger.debug("GRIND State")
        self.persistent_state['farming'] = previous_state.persistent_state.get('farming', False)

        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

        self._looting_is_available = False
        self._cast_failure_policy = CastFailurePolicy(self.controller)
        self._last_target_switch = time.time()
        self._is_pulling = False
        self._is_attacking = False

    def interpret(self, character: Character, target: Target, screen: Image):
        if character.hp == 0:
            self.persistent_state['corpse_position'] = character.position
            character.current_waypoint = 0
            return

        if target.hp > 0:
            self._is_pulling = True
            return

        if self.persistent_state['farming'] and not character.is_in_combat:
            self.persistent_state['farming'] = False
            self._looting_is_available = True

        if not character.is_in_combat:
            for action in self.behavior.interpret('non_combat', character, target):
                action.execute(self.controller)
            self.waypoint_follower.move(character)
            if time.time() - self._last_target_switch > GlobalConfig.config.combat.targeting_frequency:
                self.controller.switch_target()
                self._last_target_switch = time.time()
        else:
            self.persistent_state['farming'] = True
            self._is_attacking = True

    def transition(self, character: Character, target: Target, screen: Image) -> 'BaseState' or None:
        if self.persistent_state.get('corpse_position', None):
            return DeadState(self.controller, self.behavior, self.waypoints, self)
        if self._looting_is_available:
            return LootState(self.controller, self.behavior, self.waypoints)
        if self._is_attacking:
            return CombatState(self.controller, self.behavior, self.waypoints, self)
        if self._is_pulling:
            return PullState(self.controller, self.behavior, self.waypoints, self)


