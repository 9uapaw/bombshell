import math

from core.position.position import Trajectory, Direction
from core.position.util import calculate_trajectory, calculate_turn, calculate_turn_from_trajectory
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, RAD_PER_TURN
from exception.core import PrerequisiteException
from game.character import Character
from game.states.base import BaseState
from game.states.move import MoveState
from game.target import Target


class StartState(BaseState):

    def interpret(self, character: Character, target: Target):
        current_trajectory = calculate_trajectory(character.position, character.facing)
        waypoint_trajectory = Trajectory(character.position, self.waypoints.waypoints[character.current_waypoint])

        angle, direction = calculate_turn_from_trajectory(current_trajectory, waypoint_trajectory)

        if direction == Direction.left:
            self.controller.turn_left(math.ceil(angle * RAD_PER_TURN))
        else:
            self.controller.turn_right(math.ceil(angle * RAD_PER_TURN))

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        if character.position.is_close_to(self.waypoints.waypoints[character.current_waypoint],
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            return MoveState(self.controller, self.behavior, self.waypoints)
        else:
            raise PrerequisiteException('Waypoint is {} yards away'.format(
                character.position.calculate_distance_from(self.waypoints.waypoints[character.current_waypoint])))
