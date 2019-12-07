from core.config import GlobalConfig
from core.data import DistanceRange
from game.states.combat import CombatState
from game.states.decision_tree.common_decisions import DecisionPredicateNode, StateTransitionExecutable, VoidExecutable, \
    DecisionTickNode, ControllerMethodsExecutable
from game.states.pull import PullState

GRIND_DECISIONS = lambda: [
    DecisionPredicateNode("1", [''], executable=StateTransitionExecutable(CombatState, "Character is in combat."),
                          predicate=lambda frame, state: frame.character.is_in_combat),
    DecisionPredicateNode("2", [''], executable=StateTransitionExecutable(PullState, "Target is alive and in range."),
                          predicate=lambda frame, state: frame.target.hp > 0 and (
                                  frame.target.distance == DistanceRange.cast or frame.target.distance == DistanceRange.melee)),
    DecisionPredicateNode("3", [''], executable=None, predicate=lambda frame, state: not frame.character.is_in_combat),
    DecisionTickNode("4", ['3'], time=GlobalConfig.config.combat.targeting_frequency,
                     executable=ControllerMethodsExecutable(methods={('switch_target', [])}))
]
