import operator
import time

from core.logger import Logger
from etc.const import GREATER, GREATER_EQUALS, LESS, LESS_EQUALS, EQUALS, NOT_EQUALS, VOID
from game.behavior.action import BehaviorAction, CastAction, NullAction
from game.behavior.map import OPERATORS, ATTRIBUTES, VALUE_MAP
from game.player.character import Character
from game.target import Target


class BehaviorEntry:

    def __init__(self, index: int, parent: [int], behavior: dict):
        self.behavior = behavior
        self.index = index
        self.parent = parent

    def get_action(self) -> BehaviorAction:
        return NullAction(self.behavior) if self.behavior['actions'] == VOID else CastAction(self.behavior)

    def check(self, character: Character, target: Target) -> bool:
        raise NotImplementedError()


class BehaviorNode(BehaviorEntry):

    def __init__(self, index: int, parent: [int], behavior: dict):
        super().__init__(index, parent, behavior)
        self._last_tick = 0

    def check(self, character: Character, target: Target) -> bool:
        attr = None

        if self.behavior['unit'] == 'Character':
            mapped_attr = ATTRIBUTES['Character'].get(self.behavior['attrs'], '')
            attr = getattr(character, mapped_attr if mapped_attr else self.behavior['attrs'])
        elif self.behavior['unit'] == 'Target':
            mapped_attr = ATTRIBUTES['Target'].get(self.behavior['attrs'], '')
            attr = getattr(target, mapped_attr if mapped_attr else self.behavior['attrs'])
        elif self.behavior['unit'] == 'Tick':
            attr = time.time() - self._last_tick

        self._last_tick = time.time()
        comparable_value = VALUE_MAP[self.behavior['attrs']](self.behavior['attr_value'])

        res = OPERATORS[self.behavior['attrs']][self.behavior['ops']](attr, comparable_value)
        Logger.debug("Attribute: {} {} {} = {}".format(attr, self.behavior['ops'], comparable_value, res))

        return res
