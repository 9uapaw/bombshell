from PIL import Image

from core.config import GlobalConfig
from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower
from exception.core import PrerequisiteException
from game.player.character import Character
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.grind import GrindState
from game.states.move import MoveState
from game.target import Target


class StartState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(controller, self.waypoints)

    def interpret(self, character: Character, target: Target, screen: Image = None):
        closes_waypoint_index = self.waypoints.waypoints.index(min(self.waypoints.waypoints, key=character.position.calculate_distance_from))
        character.current_waypoint = closes_waypoint_index

        self.waypoint_follower.turn(character)

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        if character.position.is_close_to(self.waypoints.peek(character.current_waypoint),
                                          GlobalConfig.config.movement.waypoint_difference_threshold):
            return GrindState(self.controller, self.behavior, self.waypoints, self)
        else:
            raise PrerequisiteException('Waypoint is {} yards away'.format(
                character.position.calculate_distance_from(self.waypoints.waypoints[character.current_waypoint])))

