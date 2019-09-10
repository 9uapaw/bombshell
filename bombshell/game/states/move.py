from typing import List

from game.control.follow import PositionFollower
from game.position.position import Position, Direction
from game.position.transform import transform_turn
from game.position.waypoint import PositionStorage
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, TURN_THRESHOLD
from game.behavior import CharacterBehavior
from game.character import Character
from game.control.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self._coords = []  # type: List[Position]
        self.waypoint_follower = PositionFollower(self.controller, )

    def interpret(self, character: Character, target: Target):
        if character.position.is_close_to(self.waypoints.waypoints[character.current_waypoint],
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            character.is_moving = False
            self.controller.stop()

            if character.current_waypoint == len(self.waypoints.waypoints):
                character.current_waypoint = 0
            else:
                character.current_waypoint += 1

        if len(self._coords) == 0 or character.position != self._coords[-1]:
            self._coords.append(character.position)

        self.waypoint_follower.move_to(character, self.waypoints.peek(character.current_waypoint))

    def transition(self, character: Character, target: Target) -> BaseState or None:
        pass
