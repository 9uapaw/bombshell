from PIL import Image

from core.config import GlobalConfig
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower

from game.player.character import Character
from game.position.position import Position
from game.position.transform import find_best_waypoint_route
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
import game.states.grind
from game.target import Target
from image.screenscuttler import ScreenScuttler, ScreenObjects


class DeadState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: BaseState = None):
        super().__init__(controller, behavior, waypoints)
        self.scuttler = ScreenScuttler()
        self.movement = PositionFollower(self.controller, self.waypoints)

        self._released = False
        self._close_to_corpse = False
        self._state = previous_state

        closest_waypoint_route = find_best_waypoint_route([wp['waypoints'] for wp in GlobalConfig.config.waypoint['ghost']], previous_state.transition_data['corpse_position'])
        self.waypoints.parse(GlobalConfig.config.waypoint['ghost'][closest_waypoint_route])

    def interpret(self, character: Character, target: Target, screen: Image = None):
        if not self._released:
            release_button = self.scuttler.find(screen, ScreenObjects.RELEASE_BUTTON)
            if release_button:
                self.controller.click_in_middle(release_button)
                self._released = True
        else:
            accept_button = self.scuttler.find(screen, ScreenObjects.ACCEPT_BUTTON)
            if accept_button:
                self.controller.stop()
                self.controller.click_in_middle(accept_button)
                self._close_to_corpse = True
            else:
                self.movement.move(character)

        pass

    def transition(self, character: Character, target: Target, screen: Image) -> 'BaseState' or None:
        if self._close_to_corpse:
            return game.states.grind.GrindState(self.controller, self.behavior, self.waypoints)

