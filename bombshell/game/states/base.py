from game.behavior import CharacterBehavior
from game.character import Character
from game.control import CharacterController
from game.target import Target


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior):
        self.controller = controller
        self.behavior = behavior

    def interpret(self, character: Character, target: Target):
        raise NotImplementedError()

    def transition_to_combat(self):
        raise NotImplementedError()

    def transition_to_move(self):
        raise NotImplementedError()

    def transition_to_rest(self):
        raise NotImplementedError()
