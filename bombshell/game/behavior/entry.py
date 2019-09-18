import operator

from etc.const import GREATER, GREATER_EQUALS, LESS, LESS_EQUALS, EQUALS, NOT_EQUALS, VOID
from game.behavior.action import BehaviorAction, CastAction, NullAction
from game.behavior.map import OPERATORS
from game.player.character import Character
from game.target import Target


class BehaviorEntry:

    def get_action(self) -> BehaviorAction:
        raise NotImplementedError()

    def check(self, character: Character, target: Target) -> bool:
        raise NotImplementedError()


class BehaviorNode(BehaviorEntry):

    def __init__(self, index: int, parent: [int], behavior: dict):
        self.behavior = behavior
        self.index = index
        self.parent = parent

    def get_action(self) -> BehaviorAction:
        return NullAction(self.behavior) if self.behavior['action'] == VOID else CastAction(self.behavior)

    def check(self, character: Character, target: Target) -> bool:
        attr = None

        if self.behavior['unit'] == 'character':
            attr = getattr(character, self.behavior['attr'])
        elif self.behavior['unit'] == 'target':
            attr = getattr(target, self.behavior['attr'])

        return OPERATORS[self.behavior['op']](attr, self.behavior['value'])
