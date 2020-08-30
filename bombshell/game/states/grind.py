import time

from core.config import GlobalConfig
from core.data import DistanceRange
from core.frame import Frame
from core.logger import Logger
from exception.core import UnrecoverableException
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower
from game.player.attributes import LastAbilityExecution
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
from game.states.combat.combat import CombatState
from game.states.dead import DeadState
from game.states.facing_wrong import FacingWrongRecoveryState
from game.states.move.move import MoveState
from game.states.pull import PullState
from game.states.simple_loot import SimpleLootState


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

        self._last_target_switch = time.time()
        self.create_sub_state(MoveState)

    def interpret(self, frame: Frame):
        if frame.character.hp == 0:
            frame.character.is_moving = False
            self.log("Character is dead. Executing dead protocol")

            if 'ghost' not in GlobalConfig.config.waypoint:
                raise UnrecoverableException("No ghost waypoint defined")

            self.persistent_state['corpse_position'] = frame.character.position
            frame.character.current_waypoint = 0
            self.set_next_state(DeadState)
            time.sleep(2)
            return

        if frame.character.is_in_combat and not self.is_current_sub_state(PullState):
            if self.create_sub_state(CombatState):
                self.log("Character is in combat.")
                return

        if frame.target.hp > 0 and (
                frame.target.distance == DistanceRange.cast or frame.target.distance == DistanceRange.melee) and not frame.character.is_in_combat:
            if self.create_sub_state(PullState):
                self.log("Target is alive and is in range.")
                return

        self.interpret_sub_state(frame)

        if not frame.character.is_in_combat and not self.is_current_sub_state(PullState):
            while self.do_behavior('non_combat', frame.character, frame.target):
                pass
            else:
                if time.time() - self._last_target_switch > GlobalConfig.config.combat.targeting_frequency and self.is_current_sub_state(
                        MoveState):
                    self.log("Switched target")
                    self.controller.switch_target()
                    self._last_target_switch = time.time()
