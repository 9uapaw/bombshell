import operator

from etc.const import GREATER, GREATER_EQUALS, LESS, LESS_EQUALS, EQUALS, NOT_EQUALS

ATTRIBUTES = {
    'Character': {
        'health': 'hp',
        'resource': 'resource',
        'is in combat': 'is_in_combat',
        'has pet': 'has_pet',
        'first class resource': 'first_class_resource',
        'pet health': 'pet_hp',
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
    "has pet": _DISCRETE,
    "first class resource": _DISCRETE,
    "health": _CONTINOUS,
    "pet health": _CONTINOUS,
    "resource": _CONTINOUS,
    "distance": _DISCRETE,
    "second": _CONTINOUS
}

_DISTANCE_VALUES = {"25 yard": 2, "8 yard": 1, "out of range": 0}
VALUE_CONVERTER = {
    "distance": lambda d: _DISTANCE_VALUES[d],
    "is in combat": lambda c: {"True": True, "False": False}[c],
    "has pet": lambda c: {"True": True, "False": False}[c],
    "first class resource": lambda c: {"True": True, "False": False}[c],
    "health": int,
    "resource": int,
    "second": float,
    "pet health": int
}
