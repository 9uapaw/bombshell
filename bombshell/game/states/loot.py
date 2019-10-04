from config import Config
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.target import Target
from grind import GrindState
from screen import Screen
from screenscuttler import ScreenScuttler


class LootState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, config: Config, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.engaged = False
        self.config = config
        self.screen = Screen(self.config.screen_res)
        self.scuttler = ScreenScuttler()
        self.waypoint = waypoints
        self.finished_looting = False

    def check_through_screen(self, current_screen):
        iter_x = int((self.config.screen_res[2] - self.config.screen_res[0]) / 20) + 1
        iter_y = int((self.config.screen_res[3] - self.config.screen_res[1]) / 15) + 1
        base_x = self.config.screen_res[0]
        base_y = self.config.screen_res[1]

        found = False

        for i in range(0, iter_x):
            x = base_x + iter_x * i
            for j in range(0, iter_y):
                y = base_y + iter_y * j
                self.controller.move_mouse(x, y)
                found = self.scuttler.find_loot_icon(current_screen)
                if found:
                    self.controller.right_click()

        if not found:
            self.finished_looting = True

    def interpret(self, character: Character, target: Target):
        while not self.finished_looting:
            current_screen = self.screen.capture()
            self.check_through_screen(current_screen)

    def transition(self, character: Character, target: Target) -> BaseState or None:
        if self.finished_looting:
            return GrindState(controller=self.controller, behavior=self.behavior, waypoints=self.waypoints)

