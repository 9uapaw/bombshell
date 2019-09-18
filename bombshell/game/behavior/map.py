import operator

from etc.const import GREATER, GREATER_EQUALS, LESS, LESS_EQUALS, EQUALS, NOT_EQUALS
from game.behavior.action import CastAction, NullAction

UNIT = {
    'Character': 'character',
    'Target': 'target'
}

ATTRIBUTES = {
    'Character': {
    'health': 'hp',
    'resource': 'resource',
    'is in combat': 'is_in_combat'
    },
    'Target': {
        'health': 'hp',
        'resource': 'resource'
    }
}

OPERATORS = {
    "bool": {
        EQUALS: operator.eq
    },
    "int": {
        GREATER: operator.gt,
        GREATER_EQUALS: operator.ge,
        LESS: operator.lt,
        LESS_EQUALS: operator.le,
        EQUALS: operator.eq,
        NOT_EQUALS: operator.ne
    }
}

ACTIONS = {
    'cast': 'Cast',
    'do nothing': 'Void'
}
