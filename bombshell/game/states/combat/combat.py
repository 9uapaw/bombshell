from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.combat.attack import AttackState
from game.states.move import MoveState


class CombatState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self.set_current_sub_state(AttackState)

    def interpret(self, frame: Frame):
        self.interpret_sub_state(frame)

        if not frame.character.is_in_combat:
            self.next_state = MoveState
