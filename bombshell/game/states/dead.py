from typing import Tuple

from core.config import Config
from core.logger import Logger
from follow import PositionFollower
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.target import Target
import game.states.grind
from image.screen import Screen
from image.screenscuttler import ScreenScuttler, ScreenObjects


class DeadState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        Logger.debug('Dead state')
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)
        self.screen = Screen(self.screen_res)
        self.scuttler = ScreenScuttler()
        # hogy adjuk be neki a dead waypointot?
        self.waypoint = waypoints
        self.final_wp = False
        self.alive = False

    def interpret(self, character: Character, target: Target):
        self.waypoint_follower.move(character)
        if len(self.waypoints.waypoints) - 1 == character.current_waypoint:
            # ez így nyilván nem jó de hasonló logika kéne
            self.final_wp = True

        if self.alive and self.final_wp:
            accept_btn = self.scuttler.find_in_screen(ScreenObjects.ACCEPT_BUTTON)
            self.controller.click_in_middle(accept_btn)

    def transition(self, character: Character, target: Target) -> BaseState or None:
        if self.final_wp and self.final_wp:
            return LAST_STATE jön ide

