import time
from typing import List, Type, Set, Tuple

from core.frame import Frame
from core.logger import Logger
from game.states.base import BaseState
from game.states.decision_tree.node import DecisionExecutable, DecisionNode


class VoidExecutable(DecisionExecutable):

    def execute(self, state: BaseState):
        Logger.info("No decision found. This could be an error in the definition of the decision tree.")


class StateTransitionExecutable(DecisionExecutable):

    def __init__(self, state: Type[BaseState], description: str):
        self._state_type = state
        self._description = description

    def execute(self, state: BaseState):
        Logger.info(self._description)

        state.set_current_sub_state(self._state_type)


class ControllerMethodsExecutable(DecisionExecutable):

    def __init__(self, methods: Set[Tuple[str, List]]):
        self._methods = methods

    def execute(self, state: BaseState):
        Logger.info("Executing controls: {}".format(self._methods))
        for method_name, arg in self._methods:
            getattr(state.controller, method_name)(*arg)


class DecisionTickNode(DecisionNode):

    def __init__(self, index: str, parent: List[str], **kwargs):
        super().__init__(index, parent)

        self._time = kwargs['time']
        self._last_time = time.time()
        self._executable = kwargs.get('executable', None)

    def decide(self, frame: Frame, state: BaseState) -> bool:
        if time.time() - self._last_time >= self._time:
            self._last_time = time.time()
            return True
        else:
            return False

    def get_executable(self) -> DecisionExecutable or None:
        return self._executable


class DecisionPredicateNode(DecisionNode):

    def __init__(self, index: str, parent: List[str], **kwargs):
        super().__init__(index, parent, **kwargs)

        self._executable = kwargs.get('executable', None)
        self._predicate = kwargs.get('predicate', lambda *args, **kwargs: False)

    def decide(self, frame: Frame, state: BaseState) -> bool:
        return self._predicate()

    def get_executable(self) -> DecisionExecutable or None:
        return self._executable
