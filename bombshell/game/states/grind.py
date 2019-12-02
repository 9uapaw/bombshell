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
from game.states.base import BaseState
from game.states.combat.combat import CombatState
from game.states.dead import DeadState
from game.states.facing_wrong import FacingWrongRecoveryState
from game.states.move import MoveState
from game.states.pull import PullState
from game.states.simple_loot import SimpleLootState


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

        self._last_target_switch = time.time()
        self.set_current_sub_state(MoveState)

    def interpret(self, frame: Frame):
        if frame.character.hp == 0:
            Logger.info("Character is dead. Executing dead protocol")

            if 'ghost' not in GlobalConfig.config.waypoint:
                raise UnrecoverableException("No ghost waypoint defined")

            self.persistent_state['corpse_position'] = frame.character.position
            frame.character.current_waypoint = 0
            self.next_state = DeadState(self.controller, self.behavior, self.waypoints, self)
            return

        if frame.character.is_in_combat and type(self.current_state) != PullState:
            if self.set_current_sub_state(CombatState):
                Logger.info("Character is in combat.")
                return

        if frame.target.hp > 0 and (frame.target.distance == DistanceRange.cast or frame.target.distance == DistanceRange.melee) and not frame.character.is_in_combat:
            if self.set_current_sub_state(PullState):
                Logger.info("Target is alive and is in range.")
                return

        self.interpret_sub_state(frame)

        if not frame.character.is_in_combat:
            while self.do_behavior('non_combat', frame.character, frame.target):
                pass
            else:
                if time.time() - self._last_target_switch > GlobalConfig.config.combat.targeting_frequency and type(self.current_state) == MoveState:
                    Logger.info("Switched target")
                    self.controller.switch_target()
                    self._last_target_switch = time.time()



