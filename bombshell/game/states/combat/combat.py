from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
from game.states.combat.attack import AttackState
from game.states.move.move import MoveState
from game.states.simple_loot import SimpleLootState


class CombatState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.create_sub_state(AttackState)

    def interpret(self, frame: Frame):
        self.interpret_sub_state(frame)

        if not frame.character.is_in_combat and not self.is_current_sub_state(SimpleLootState):
            self.set_next_state(MoveState)
