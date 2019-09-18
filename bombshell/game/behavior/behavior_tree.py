from typing import Dict, Tuple, List, Iterable

from game.behavior.action import BehaviorAction
from game.behavior.entry import BehaviorNode
from game.control.control import CharacterController
from game.player.character import Character
from game.target import Target


class BehaviorTree:

    def __init__(self):
        self._tree = {}  # type: Dict[int, List[BehaviorNode]]

    def add(self, node: BehaviorNode):
        for p in node.parent:
            if p in self._tree:
                self._tree[p].append(node)
            else:
                self._tree[p] = [node]

    def traverse(self, character: Character, target: Target) -> Iterable[BehaviorAction]:
        if 0 not in self._tree:
            return

        yield self._traverse([0], character, target)

    def _traverse(self, parent_indexes: List[int], character: Character, target: Target) -> Iterable[BehaviorAction]:
        for parent_index in parent_indexes:
            for node in self._tree[parent_index]:
                if node.check(character, target):
                    yield node.get_action()
                    self._traverse(node.parent, character, target)


