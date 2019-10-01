import operator

from etc.const import GREATER, GREATER_EQUALS, LESS, LESS_EQUALS, EQUALS, NOT_EQUALS

UNIT = {
    'Character': 'character',
    'Target': 'target',
    'Tick': 'tick'
}

ATTRIBUTES = {
    'Character': {
        'health': 'hp',
        'resource': 'resource',
        'is in combat': 'is_in_combat'
    },
    'Target': {
        'health': 'hp',
        'resource': 'resource',
        'distance': 'distance'
    },
    'Tick': {
        'second': 'second'
    }
}

_DISCRETE = {EQUALS: operator.eq}
_CONTINOUS = {
    GREATER: operator.gt,
    GREATER_EQUALS: operator.ge,
    LESS: operator.lt,
    LESS_EQUALS: operator.le,
    EQUALS: operator.eq,
    NOT_EQUALS: operator.ne
}

OPERATORS = {
    "is in combat": _DISCRETE,
    "health": _CONTINOUS,
    "resource": _CONTINOUS,
    "distance": _DISCRETE,
    "second": _CONTINOUS
}

_PERCENT_VALUES = list(map(str, range(0, 101)))
_DISTANCE_VALUES = {"25 yard": 2, "8 yard": 1, "out of range": 0}
_BOOLEAN_VALUES = ["True", "False"]
_TIME_VALUES = list(map(str, [1, 2, 2.5, 3, 5, 10, 50, 100, 500, 1000, 1800, 3600]))
VALUE_MAP = {
    "distance": lambda d: _DISTANCE_VALUES[d],
    "is in combat": lambda c: {"True": True, "False": False}[c],
    "health": int,
    "resource": int,
    "second": float
}
ATTR_VALUES = {
    "is in combat": _BOOLEAN_VALUES,
    "health": _PERCENT_VALUES,
    "resource": _PERCENT_VALUES,
    "distance": list(_DISTANCE_VALUES.keys()),
    "second": _TIME_VALUES
}

ACTIONS = {
    'cast': 'Cast',
    'do nothing': 'Void'
}
