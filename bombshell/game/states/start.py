import math

from matplotlib.lines import Line2D

from game.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower
from game.position.position import Trajectory, Direction, CharacterDirection
from game.position.transform import calculate_trajectory, transform_turn
from etc.const import WAYPOINT_DIFFERENCE_THRESHOLD, TURN_THRESHOLD
from exception.core import PrerequisiteException
from game.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.move import MoveState
from game.target import Target
import matplotlib.pyplot as plt


class StartState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(controller)

    def interpret(self, character: Character, target: Target):
        self.waypoint_follower.turn_to(CharacterDirection(character.position, character.facing), self.waypoints.peek(character.current_waypoint))

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        if character.position.is_close_to(self.waypoints.peek(character.current_waypoint),
                                          WAYPOINT_DIFFERENCE_THRESHOLD):
            return MoveState(self.controller, self.behavior, self.waypoints)
        else:
            raise PrerequisiteException('Waypoint is {} yards away'.format(
                character.position.calculate_distance_from(self.waypoints.waypoints[character.current_waypoint])))

