from PIL import Image

from core.config import GlobalConfig
from core.frame import Frame
from etc.const import RELEASE_SPIRIT, ACCEPT_REZ
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower

from game.player.character import Character
from game.position.position import Position
from game.position.transform import find_best_waypoint_route
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
import game.states.grind
from game.states.move.move import MoveState
from game.target import Target
from image.screenscuttler import ScreenScuttler, ScreenObjects


class DeadState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.scuttler = ScreenScuttler()
        self._released = False

        closest_waypoint_route = find_best_waypoint_route(
            [[Position(w[0], w[1]) for w in wp['waypoints']] for wp in GlobalConfig.config.waypoint['ghost']],
            transition_state.persistent_state['last_position'])
        self.waypoints.parse(GlobalConfig.config.waypoint['ghost'][closest_waypoint_route]['waypoints'])

        self.set_current_sub_state(MoveState)

    def interpret(self, frame: Frame):
        if not self._released:
            # release_button = self.scuttler.find(frame.screen, ScreenObjects.RELEASE_BUTTON)
            # if release_button:
            #     self.controller.click_in_middle(release_button)
            #     self._released = True
            self.controller.write(RELEASE_SPI.RIT)
            self._released = True

        else:
            if frame.character.hp == 0:
                self.interpret_sub_state(frame)
                self.controller.write(ACCEPT_REZ)
            else:
                self.set_next_state(game.states.grind.GrindState)

            # accept_button = self.scuttler.find(frame.screen, ScreenObjects.ACCEPT_BUTTON)
            # if accept_button:
            #     self.controller.stop()
            #     self.controller.click_in_middle(accept_button)
            #     self._close_to_corpse = True
            # else:
            #     self.movement.move(frame.character)

        pass
