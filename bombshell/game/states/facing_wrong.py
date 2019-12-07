import time

from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.follow import PositionFollower
from game.player.attributes import LastAbilityExecution
from game.position.waypoint import PositionStorage
from game.control.control import CharacterController
from game.states.base import BaseState, TransitionType
import game.states.combat.attack


class FacingWrongRecoveryState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: 'BaseState' = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

    def interpret(self, frame: Frame):
        if frame.character.last_ability in (LastAbilityExecution.NOT_INFRONT, LastAbilityExecution.OUT_OF_LOS):
            self.log("Facing the wrong way. Turning around.")
            self.controller.interact_with_target()
            time.sleep(2)
        else:
            self.set_next_state(game.states.combat.attack.AttackState)
