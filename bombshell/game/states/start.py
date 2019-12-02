
from core.config import GlobalConfig
from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.control.follow import PositionFollower
from exception.core import PrerequisiteException
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.states.grind import GrindState
import game.states.dead


class StartState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(controller, self.waypoints)
        self._next_state = None

    def interpret(self, frame: Frame):
        if frame.character.hp == 0:
            self.persistent_state['last_position'] = frame.character.position
            self._next_state = game.states.dead.DeadState(self.controller, self.behavior, self.waypoints, self)

            return

        closes_waypoint_index = self.waypoints.waypoints.index(min(self.waypoints.waypoints, key=frame.character.position.calculate_distance_from))
        frame.character.current_waypoint = closes_waypoint_index

        self.waypoint_follower.turn(frame.character)

    def transition(self, frame: Frame) -> 'BaseState' or None:
        if self._next_state:
            return self._next_state

        if frame.character.position.is_close_to(self.waypoints.peek(frame.character.current_waypoint),
                                          GlobalConfig.config.movement.waypoint_difference_threshold):
            return GrindState(self.controller, self.behavior, self.waypoints, self)
        else:
            raise PrerequisiteException('Waypoint is {} yards away'.format(
                frame.character.position.calculate_distance_from(self.waypoints.waypoints[frame.character.current_waypoint])))

