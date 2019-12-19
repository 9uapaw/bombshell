from typing import List

from PIL import Image

from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.player.character import Character
from game.control.control import CharacterController
from game.states.base import BaseState, TransitionType
from game.states.move.stuck import StuckResolverState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: 'BaseState' = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.set_current_sub_state(StuckResolverState)

    def interpret(self, frame: Frame):
        self.waypoint_follower.move(frame.character)
        self.interpret_sub_state(frame)
