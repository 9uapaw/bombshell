from typing import Dict, List

from core.frame import Frame
from game.states.base import BaseState
from game.states.decision_tree.common_decisions import VoidExecutable
from game.states.decision_tree.node import DecisionNode, DecisionExecutable


class DecisionTree:

    def __init__(self):
        self._tree = {}  # type: Dict[str, List[DecisionNode]]

    def add(self, node: DecisionNode):
        for p in node.parent:
            if p in self._tree:
                self._tree[p].append(node)
            else:
                self._tree[p] = [node]

    def traverse(self, frame: Frame, state: BaseState) -> DecisionExecutable:
        if '' not in self._tree:
            return VoidExecutable()

        return self._traverse([''], frame, state)

    def _traverse(self, parent_indexes: List[str], frame: Frame, state: BaseState) -> DecisionExecutable:
        for parent_index in parent_indexes:
            for node in self._tree.get(parent_index, []):
                if node.decide(frame, state):
                    exe = node.get_executable()
                    if exe:
                        return exe
                    else:
                        return self._traverse(node.parent, frame, state)

        return VoidExecutable()

