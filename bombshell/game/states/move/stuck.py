import math
import random
from functools import reduce

from core.config import GlobalConfig
from core.frame import Frame
from core.util import FixedList
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.position.position import Position, Direction
from game.position.waypoint import PositionStorage
from game.states.base import BaseState, TransitionType


class StuckResolverState(BaseState):
    LAST_N_POSITION = GlobalConfig.config.movement.stuck_last_n_position

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: 'BaseState' = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        super().__init__(controller, behavior, waypoints, transition_state)
        self._positions = FixedList(10)
        self._jumps = 0
        self._direction = None

    def interpret(self, frame: Frame):
        self._positions.append(frame.character.position)

        if len(self._positions.data) >= self.LAST_N_POSITION + 1:
            # distance_from_last_position = self._positions.data[-1].calculate_distance_from(self._positions.data[-2])
            x_avg = 0
            y_avg = 0
            for i in range(len(self._positions.data) - 1, len(self._positions.data) - self.LAST_N_POSITION - 1, -1):
                x_avg += self._positions.data[i].x
                y_avg += self._positions.data[i].y

            x_avg = x_avg / self.LAST_N_POSITION
            y_avg = y_avg / self.LAST_N_POSITION

            avg_point = Position(x_avg, y_avg)
            distance_from_last_position = self._positions.data[-1].calculate_distance_from(avg_point)

            if self._direction:
                self.controller.turn(self._direction, random.uniform(GlobalConfig.config.movement.stuck_turn_range[0],
                                                                     GlobalConfig.config.movement.stuck_turn_range[1]))
            elif self._jumps >= GlobalConfig.config.movement.stuck_first_level_threshold:
                self._direction = Direction(random.randint(0, 1))

            if distance_from_last_position <= GlobalConfig.config.movement.stuck_threshold:
                self.log("Character is stuck, pressing space.")
                self.controller.cast_spell('space')
                self._jumps += 1
            else:
                self._jumps = 0
                self._direction = None



