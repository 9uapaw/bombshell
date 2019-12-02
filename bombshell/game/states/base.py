from typing import Type

from PIL import Image

from core.frame import Frame
from core.logger import Logger
from game.position.waypoint import PositionStorage
from game.behavior.character_behavior import CharacterBehavior
from game.player.character import Character
from game.control.control import CharacterController
from game.target import Target


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: 'BaseState' = None):
        Logger.info("Initiating {}".format(self.__class__.__name__))
        self.controller = controller
        self.behavior = behavior
        self.waypoints = waypoints
        self.persistent_state = {}
        self.behavior_interpretation = {}
        self.current_state = None  # type: 'BaseState' or None
        self.next_state = None  # type: 'BaseState' or None

    def interpret(self, frame: Frame):
        raise NotImplementedError()

    def transition(self, frame: Frame) -> 'BaseState' or None:
        return self.next_state

    def interpret_sub_state(self, frame: Frame):
        if self.current_state:
            self.current_state.interpret(frame)
            transition = self.current_state.transition(frame)

            if transition:
                Logger.info("Current substate: {} requests transition to: {}".format(self.current_state.__class__.__name__, transition.__name__))
                self.set_current_sub_state(transition)

    def set_current_sub_state(self, state: Type['BaseState']) -> bool:
        if type(self.current_state) != state:
            Logger.info("Transitioning to subsate: {} of mainstate: {}".format(state.__name__, self.__class__.__name__))
            self.current_state = state(self.controller, self.behavior, self.waypoints, self)
            return True
        else:
            return False

    def do_behavior(self, behavior_type: str, character: Character, target: Target) -> bool:
        behavior = self.behavior_interpretation.get(behavior_type, None)
        if behavior is None:
            self.behavior_interpretation[behavior_type] = behavior = self.behavior.interpret(behavior_type)
            next(behavior)

        try:
            action = behavior.send((character, target))

            if action:
                if character.is_moving:
                    character.is_moving = False
                    self.controller.stop()
                action.execute(self.controller)
            return True
        except StopIteration:
            self.behavior_interpretation[behavior_type] = None
            return False

    def log(self, message: str):
        Logger.info("<{}>:{}".format(self.__class__.__name__, message))

