from typing import Tuple

from PIL import Image

from core.config import Config
from core.frame import Frame
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


class LootState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self.engaged = False
        self.screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)
        self.screen = Screen(self.screen_res)
        self.scuttler = ScreenScuttler()
        self.waypoint = waypoints
        self.finished_looting = False

    def interpret(self, frame: Frame):
        while not self.finished_looting:
            gen = self.screen.capture()
            self._check_through_screen(gen)

    def transition(self, frame: Frame) -> BaseState or None:
        if self.finished_looting:
            return game.states.grind.GrindState(controller=self.controller, behavior=self.behavior, waypoints=self.waypoints, previous_state=self)

    def _check_through_screen(self, gen):
        Logger.debug("Entered loot state - Checking through screen")
        max_step_x = 20
        max_step_y = 15
        iter_x = int((self.screen_res[2] - self.screen_res[0]) / max_step_x) + 1
        iter_y = int((self.screen_res[3] - self.screen_res[1]) / max_step_y) + 1
        base_x = self.screen_res[0]
        base_y = self.screen_res[1]

        safe_zone = 3
        max_step_x -= safe_zone
        max_step_y -= safe_zone

        Logger.debug("Checking through screen: x-stepsize: {} y-stepsize: {}".format(iter_x, iter_y))

        found = False

        while True:
            for i in range(safe_zone, max_step_x):
                x = base_x + iter_x * i
                for j in range(safe_zone*2, max_step_y): # start from more downwards
                    y = base_y + iter_y * j
                    Logger.debug("Current x: {} current y: {}".format(x, y))
                    self.controller.move_mouse(x, y)
                    current_screen = next(gen)
                    found = self.scuttler.try_find(current_screen, ScreenObjects.LOOT_ICON.value)
                    if found:
                        self.controller.right_click()
            if not found:
                break

        if not found:
            self.finished_looting = True

