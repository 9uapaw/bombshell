from typing import Dict, Tuple, Iterable, Generator

from game.behavior.action import BehaviorAction
from game.behavior.behavior_tree import BehaviorTree
from game.behavior.entry import CharacterNode
from game.player.character import Character
from game.control.control import CharacterController
from game.target import Target


class CharacterBehavior:

    def __init__(self):
        self.behavior_trees = {}  # type: Dict[(str, BehaviorTree)]

    def resolve_profile(self, behavior: dict):
        for behavior_type, nodes in behavior.items():
            tree = BehaviorTree()
            for n in nodes:
                node = CharacterNode(n['key'], n['parent'], n['behavior'])
                tree.add(node)
            self.behavior_trees[behavior_type] = tree

    def interpret(self, behavior_type: str) -> Generator[BehaviorAction, Tuple[Character, Target], None]:
        return self.behavior_trees[behavior_type].traverse()
