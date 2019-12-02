import time

from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.follow import PositionFollower
from game.player.attributes import LastAbilityExecution
from game.position.waypoint import PositionStorage
from game.control.control import CharacterController
from game.states.base import BaseState
import game.states.combat.attack


class FacingWrongRecoveryState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: 'BaseState' = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

    def interpret(self, frame: Frame):
        if frame.character.last_ability in (LastAbilityExecution.NOT_INFRONT, LastAbilityExecution.OUT_OF_LOS):
            self.controller.interact_with_target()
            time.sleep(2)
        else:
            self.next_state = game.states.combat.attack.AttackState
