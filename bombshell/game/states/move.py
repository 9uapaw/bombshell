from game.character import Character
from game.states.base import BaseState
from game.target import Target


class MoveState(BaseState):

    def interpret(self, character: Character, target: Target):
        pass