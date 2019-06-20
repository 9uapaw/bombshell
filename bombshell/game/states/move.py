import math
from typing import List

from core.data import ExtractedData
from core.position import Position, Trajectory, Direction
from core.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character import Character
from game.control import CharacterController
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):
    WAYPOINT_DIFFERENCE_THRESHOLD = 0.1
    TURN_THRESHOLD = 0.1
    RAD_PER_TURN = 0.05

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self._coords = []  # type: List[Position]

    def interpret(self, character: Character, target: Target):
        if character.position.is_close_to(self.waypoints.waypoints[character.current_waypoint]):
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
            char_trajectory = Trajectory(self._coords[-1], self._coords[-2])
            waypoint_trajectory = Trajectory(self._coords[-1], self.waypoints.waypoints[character.current_waypoint])

            angle = char_trajectory.calculate_angle(waypoint_trajectory)
            direction = char_trajectory.calculate_direction(waypoint_trajectory)

            if angle >= self.TURN_THRESHOLD:
                self.controller.stop()
                character.is_moving = False
                if direction == Direction.right:
                    self.controller.turn_right(math.ceil(angle / self.RAD_PER_TURN))
                else:
                    self.controller.turn_right(math.ceil(angle / self.RAD_PER_TURN))

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        pass


