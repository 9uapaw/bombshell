import time

from PIL import Image

from core.config import GlobalConfig
from core.data import DistanceRange
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
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
        self.persistent_state['farming'] = previous_state.persistent_state.get('farming', False)

        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

        self._cast_failure_policy = CastFailurePolicy(self.controller)
        self._last_target_switch = time.time()
        self._next_state = None

    def interpret(self, character: Character, target: Target, screen: Image = None):
        if character.hp == 0:
            self.persistent_state['corpse_position'] = character.position
            character.current_waypoint = 0
            self._next_state = DeadState(self.controller, self.behavior, self.waypoints, self)
            return

        if character.is_in_combat:
            self._next_state = CombatState(self.controller, self.behavior, self.waypoints, self)

        if target.hp > 0 and (target.distance == DistanceRange.cast or target.distance == DistanceRange.melee):
            self._next_state = PullState(self.controller, self.behavior, self.waypoints, self)
            return

        if not character.is_in_combat:
            for action in self.behavior.interpret('non_combat', character, target):
                action.execute(self.controller)
            self.waypoint_follower.move(character)
            if time.time() - self._last_target_switch > GlobalConfig.config.combat.targeting_frequency:
                self.controller.switch_target()
                self._last_target_switch = time.time()

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        return self._next_state


