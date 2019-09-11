from typing import List

from game.control.follow import PositionFollower
from game.position.position import Position, Direction
from game.position.transform import transform_turn
from game.position.waypoint import PositionStorage
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, TURN_THRESHOLD
from game.behavior import CharacterBehavior
from game.character.character import Character
from game.control.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)

    def interpret(self, character: Character, target: Target):
        self.waypoint_follower.move(character)

    def transition(self, character: Character, target: Target) -> BaseState or None:
        pass
