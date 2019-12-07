from typing import List

from core.frame import Frame
from game.states.base import BaseState


class DecisionExecutable:

    def execute(self, state: BaseState):
        raise NotImplementedError()


class DecisionNode:

    def __init__(self, index: str, parent: List[str], **kwargs):
        self.index = index
        self.parent = parent

    def decide(self, frame: Frame, state: BaseState) -> bool:
        raise NotImplementedError()

    def get_executable(self) -> DecisionExecutable or None:
        raise NotImplementedError()


