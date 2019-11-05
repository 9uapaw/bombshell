from typing import List

from PIL import Image

from game.behavior.behavior import CharacterBehavior
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.player.character import Character
from game.control.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

    def interpret(self, character: Character, target: Target, screen: Image = None):
        self.waypoint_follower.move(character)

    def transition(self, character: Character, target: Target, screen: Image = None) -> BaseState or None:
        pass
