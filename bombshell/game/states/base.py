import enum
from typing import Type

from PIL import Image

from core.frame import Frame
from core.logger import Logger
from game.position.waypoint import PositionStorage
from game.behavior.character_behavior import CharacterBehavior
from game.player.character import Character
from game.control.control import CharacterController
from game.target import Target


class TransitionType(enum.Enum):
    SAME_LEVEL = 'next'
    SUB_LEVEL = 'sub'


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None,
                 transition_state: 'BaseState' = None, transition: TransitionType = TransitionType.SAME_LEVEL):
        self.controller = controller
        self.behavior = behavior
        self.waypoints = waypoints
        self.persistent_state = {}
        self.behavior_interpretation = {}
        self.transition_state = transition_state
        self.current_sub_state = None  # type: 'BaseState' or None
        self.next_state = None  # type: 'BaseState' or None

        if transition_state:
            # if transition == TransitionType.SAME_LEVEL:
            #     self.level = transition_state.level
            #     self.log_prefix = "{}:{}".format(self.level, self.__class__.__name__)
            # else:
            #     self.level = "{}:{}".format(transition_state.level, self.__class__.__name__)
            #     self.log_prefix = self.level
            self.level = "{}:{}".format(transition_state.level, self.__class__.__name__)
        else:
            self.level = "{}".format(self.__class__.__name__)
            self.log_prefix = self.level

        self.log("Initiating {}".format(self.__class__.__name__))

    def interpret(self, frame: Frame):
        raise NotImplementedError()

    def transition(self, frame: Frame) -> 'BaseState' or None:
        return self.next_state

    def interpret_sub_state(self, frame: Frame) -> bool:
        if self.current_sub_state:
            self.current_sub_state.interpret(frame)
            transition = self.current_sub_state.transition(frame)

            if transition:
                self.transition_sub_state(transition)

            return True
        else:
            return False

    def transition_sub_state(self, state: 'BaseState') -> bool:
        self.log("SubState transition by previous SubState: {} -> {}".format(self.current_sub_state.__class__.__name__, state.__class__.__name__))
        self.current_sub_state = state

        return True

    def set_current_sub_state(self, state: Type['BaseState']) -> bool:
        if not self.current_sub_state:
            self.current_sub_state = state(self.controller, self.behavior, self.waypoints, self, TransitionType.SUB_LEVEL)
        elif type(self.current_sub_state) != state:
            print(self, state, self.current_sub_state)
            self.log("SubState change by ParentState: {} -> {}".format(self.current_sub_state.__class__.__name__, state.__name__))
            self.current_sub_state = state(self.controller, self.behavior, self.waypoints, self, TransitionType.SUB_LEVEL)
            return True
        else:
            return False

    def set_next_state(self, state: Type['BaseState']) -> bool:
        if not self.next_state:
            self.next_state = state(self.controller, self.behavior, self.waypoints, self.transition_state, TransitionType.SAME_LEVEL)
            return True

    def is_current_sub_state(self, state: Type['BaseState']) -> bool:
        return type(self.current_sub_state) == state

    def do_behavior(self, behavior_type: str, character: Character, target: Target) -> bool:
        behavior = self.behavior_interpretation.get(behavior_type, None)
        if behavior is None:
            self.behavior_interpretation[behavior_type] = behavior = self.behavior.interpret(behavior_type)
            next(behavior)

        try:
            node = behavior.send((character, target))

            if node:
                desc = node.behavior.get('description', '')
                if desc:
                    self.log(desc)

                if character.is_moving:
                    character.is_moving = False
                    self.controller.stop()

                action = node.get_action()
                action.execute(self.controller)

            return True
        except StopIteration:
            self.behavior_interpretation[behavior_type] = None
            return False

    def log(self, message: str):
        Logger.info("<{}>:{}".format(self.level, message))
