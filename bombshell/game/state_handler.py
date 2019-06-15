from core.data import ExtractedData
from game.behavior import CharacterBehavior
from game.character import Character
from game.control import CharacterController
from game.target import Target


class StateHandler:

    def __init__(self, character: Character, controller: CharacterController, behavior: CharacterBehavior):
        self.character = character
        self.controller = controller
        self.behavior = behavior
        self.target = None

    def update(self, data: ExtractedData):
        if not data.combat and not self.character.is_moving:
            # self.controller.move_forward()
            self.character.is_moving = True1

        self.character.hp = data.player_health
        if not self.target and data.target_health != 0:
            self.target = Target()
            self.target.hp = data.target_health

        self._interact_with_target()

    def _interact_with_target(self):
        self.behavior.interpret(self.character, self.target)

