import time

from PIL import Image

import game.states.grind
from core.config import GlobalConfig
from core.frame import Frame
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.combat.combat import CombatState
from game.states.move import MoveState
from game.target import Target


class PullState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self._previous_grind_state = previous_state
        self._last_pull = time.time()
        self._pull_flow = False

    def interpret(self, frame: Frame):
        if time.time() - self._last_pull > GlobalConfig.config.combat.wait_after_pull and not frame.character.is_in_combat:
            Logger.info("Pull was unsuccessful.")
            self.next_state = MoveState
            return

        if frame.character.is_moving:
            self.controller.stop()
            frame.character.switch_moving()

        while self.do_behavior('pull', frame.character, frame.target):
            self._pull_flow = True
        else:
            self._pull_flow = False

        if frame.character.is_in_combat and not self._pull_flow:
            self.next_state = CombatState
