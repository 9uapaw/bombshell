from typing import List

from core.position.position import Position, Direction
from core.position.transform import calculate_turn, transform_turn
from core.position.waypoint import PositionStorage
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, TURN_THRESHOLD
from game.behavior import CharacterBehavior
from game.character import Character
from game.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self._coords = []  # type: List[Position]

    def interpret(self, character: Character, target: Target):
        if character.position.is_close_to(self.waypoints.waypoints[character.current_waypoint],
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            if character.current_waypoint == len(self.waypoints.waypoints):
                character.current_waypoint = 0
            else:
                character.current_waypoint += 1

        if not character.is_moving:
            self.controller.move_forward()
            character.is_moving = True

        if len(self._coords) == 0 or character.position != self._coords[-1]:
            self._coords.append(character.position)

        if len(self._coords) >= 2:
            angle, direction = calculate_turn((self._coords[-1], self._coords[-2]), (
            self.waypoints[character.current_waypoint][0], self.waypoints[character.current_waypoint][1]))

            if angle >= TURN_THRESHOLD:
                self.controller.stop()
                character.is_moving = False
                if direction == Direction.right:
                    self.controller.turn_right(transform_turn(angle))
                else:
                    self.controller.turn_right(transform_turn(angle))

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        pass
