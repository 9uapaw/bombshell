from typing import List

from PIL import Image

from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.player.character import Character
from game.control.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: 'BaseState' = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

    def interpret(self, frame: Frame):
        self.waypoint_follower.move(frame.character)

    def transition(self, frame: Frame) -> BaseState or None:
        pass
