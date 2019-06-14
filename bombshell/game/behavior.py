from game.character import Character
from game.control import CharacterController
from game.target import Target


class CharacterBehavior:

    def __init__(self, behavior: dict, controller: CharacterController):
        self.behavior = behavior
        self.controller = controller

    def interpret(self, character: Character, target: Target):
        if character.hp < 100:
            self.controller.cast_spell(self.behavior['100']['lt'])
