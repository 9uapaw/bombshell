import math

from core.position.position import Trajectory, Direction
from core.position.transform import calculate_trajectory, transform_turn
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, RAD_PER_TURN, TURN_THRESHOLD
from exception.core import PrerequisiteException
from game.character import Character
from game.states.base import BaseState
from game.states.move import MoveState
from game.target import Target


class StartState(BaseState):

    def interpret(self, character: Character, target: Target):
        current_trajectory = calculate_trajectory(character.position, character.facing)
        waypoint_trajectory = Trajectory(character.position, self.waypoints.waypoints[character.current_waypoint])

        angle_difference, direction = current_trajectory.calculate_turn(waypoint_trajectory)
        if angle_difference <= TURN_THRESHOLD:
            return

        print('Angle: {} - Direction: {}'.format(angle_difference, direction))

        if direction == Direction.left:
            self.controller.turn_left(transform_turn(angle_difference))
        else:
            self.controller.turn_right(transform_turn(angle_difference))

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        if character.position.is_close_to(self.waypoints.peek(character.current_waypoint),
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            return MoveState(self.controller, self.behavior, self.waypoints)
        else:
            raise PrerequisiteException('Waypoint is {} yards away'.format(
                character.position.calculate_distance_from(self.waypoints.waypoints[character.current_waypoint])))
