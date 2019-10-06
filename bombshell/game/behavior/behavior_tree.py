from typing import Dict, Tuple, List, Iterable

from core.logger import Logger
from game.behavior.action import BehaviorAction
from game.behavior.entry import BehaviorNode
from game.control.control import CharacterController
from game.player.character import Character
from game.target import Target


class BehaviorTree:

    def __init__(self):
        self._tree = {}  # type: Dict[str, List[BehaviorNode]]

    def add(self, node: BehaviorNode):
        for p in node.parent:
            if p in self._tree:
                self._tree[p].append(node)
            else:
                self._tree[p] = [node]

    def traverse(self, character: Character, target: Target) -> Iterable[BehaviorAction]:
        if '' not in self._tree:
            return []

        return self._traverse([''], character, target)

    def _traverse(self, parent_indexes: List[str], character: Character, target: Target) -> Iterable[BehaviorAction]:
        for parent_index in parent_indexes:
            for node in self._tree[parent_index]:
                if node.check(character, target):
                    yield node.get_action()
                    self._traverse(node.parent, character, target)


