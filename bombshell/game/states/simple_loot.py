import time
from typing import Tuple

from PIL import Image

from core.config import Config
from core.logger import Logger
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.target import Target
import game.states.grind
from image.screen import Screen
from image.screenscuttler import ScreenScuttler, ScreenObjects


class SimpleLootState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self.engaged = False
        self.screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)
        self.screen = Screen(self.screen_res)
        self.scuttler = ScreenScuttler()
        self.waypoint = waypoints
        self.finished_looting = False

    def interpret(self, character: Character, target: Target, screen: Image = None):
        self.controller.switch_to_previous_target()
        self.controller.interact_with_target()
        time.sleep(2)

    def transition(self, character: Character, target: Target, screen: Image = None) -> BaseState or None:
        return game.states.grind.GrindState(controller=self.controller, behavior=self.behavior, waypoints=self.waypoints, previous_state=self)
