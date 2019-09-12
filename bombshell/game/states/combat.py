from game.player import Character
from game.states.base import BaseState
from game.target import Target


class CombatState(BaseState):

    def interpret(self, character: Character, target: Target):
        pass

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        pass