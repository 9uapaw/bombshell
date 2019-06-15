from game.character import Character
from game.control import CharacterController
from game.target import Target


class CharacterBehavior:

    def __init__(self, behavior: dict, controller: CharacterController):
        self.behavior = behavior
        self.controller = controller

    def interpret(self, character: Character, target: Target):
        if character.hp > 50:
            if target.hp > 60:
                self.controller.cast_spell(1)
            else:
                self.controller.cast_spell(4)
        else:
            self.controller.cast_spell(2)
