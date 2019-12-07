import time

from PIL import Image

from core.config import GlobalConfig
from core.frame import Frame
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.attributes import LastAbilityExecution
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
import game.states.grind
from game.states.facing_wrong import FacingWrongRecoveryState
from game.states.move import MoveState
from game.states.simple_loot import SimpleLootState
from game.target import Target
import game.states.loot


class AttackState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self._behavior = self.behavior.interpret('grind')

    def interpret(self, frame: Frame):
        self.controller.stop()
        frame.character.is_moving = False

        if frame.character.last_ability in (LastAbilityExecution.NOT_INFRONT, LastAbilityExecution.OUT_OF_LOS):
            self.set_next_state(FacingWrongRecoveryState)
            return

        if frame.character.is_in_combat and frame.target.hp <= 0:
            self.log("No target, but character is in combat. Switching target")
            self.controller.switch_target()

        if not frame.character.is_in_combat and not frame.character.is_inventory_full:
            self.log("Character is not in combat, but it is in CombatState. It presumably means that loot is available")
            self.set_next_state(SimpleLootState)
            return
        elif not frame.character.is_in_combat and frame.character.is_inventory_full:
            self.log("Inventory is full. Skipping loot state")

        self.do_behavior('grind', frame.character, frame.target)
