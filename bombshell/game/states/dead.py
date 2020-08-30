
from core.config import GlobalConfig
from core.frame import Frame
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController

from game.position.position import Position
from game.position.transform import find_best_waypoint_route
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType
import game.states.grind
from game.states.move.move import MoveState


class DeadState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: BaseState = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state, transition)
        self._released = False

        closest_waypoint_route = find_best_waypoint_route(
            [[Position(w[0], w[1]) for w in wp['waypoints']] for wp in GlobalConfig.config.waypoint['ghost']],
            transition_state.persistent_state['last_position'])
        self.waypoints.parse(GlobalConfig.config.waypoint['ghost'][closest_waypoint_route]['waypoints'])

        self.create_sub_state(MoveState)

    def interpret(self, frame: Frame):
        if frame.character.hp == 0:
            self.interpret_sub_state(frame)
        else:
            self.waypoints.parse(GlobalConfig.config.waypoint['grind'][0]['waypoints'])
            closes_waypoint_index = self.waypoints.waypoints.index(min(self.waypoints.waypoints, key=frame.character.position.calculate_distance_from))
            frame.character.current_waypoint = closes_waypoint_index
            self.set_next_state(game.states.grind.GrindState)
