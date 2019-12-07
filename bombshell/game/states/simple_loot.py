import time
from typing import Tuple, Type

from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
from game.states.idle import IdleState
from image.screeninterceptor import ScreenInterceptor
from image.screenscuttler import ScreenScuttler, ScreenObjects


class SimpleLootState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.engaged = False
        self.screen_res: Tuple[int, int, int, int] = (0, 40, 800, 640)
        self.screen = ScreenInterceptor(self.screen_res)
        self.scuttler = ScreenScuttler()
        self.waypoint = waypoints
        self.finished_looting = False

    def interpret(self, frame: Frame):
        self.log("Looting")
        self.controller.switch_to_previous_target()
        self.controller.interact_with_target()
        time.sleep(2)

        self.set_next_state(IdleState)
