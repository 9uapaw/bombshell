from typing import Dict, Tuple, Iterable

from game.behavior.action import BehaviorAction
from game.behavior.behavior_tree import BehaviorTree
from game.behavior.entry import BehaviorNode
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
                node = BehaviorNode(n['key'], n['parent'], n['behavior'])
                tree.add(node)
            self.behavior_trees[behavior_type] = tree

    def interpret(self, behavior_type: str, character: Character, target: Target) -> Iterable[BehaviorAction]:
        yield self.behavior_trees[behavior_type].traverse(character, target)
