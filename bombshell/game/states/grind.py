import time

from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.target import Target


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.engaged = False
        self.last_pull = None

    def interpret(self, character: Character, target: Target):
        if target.hp > 0 and not self.engaged and target.distance.value > 0:
            if character.is_moving:
                self.controller.stop()
                character.switch_moving()

            self.controller.cast_spell(2)
            self.engaged = True
            self.last_pull = time.time()

        if target.hp == 0:
            self.engaged = False

        if self.last_pull and time.time() - self.last_pull > 5 and not character.is_in_combat:
            self.engaged = False

        if not character.is_in_combat and not self.engaged:
            self.waypoint_follower.move(character)
            self.controller.cast_spell('escape')
            self.controller.switch_target()
        else:
            for action in self.behavior.interpret('grind', character, target):
                action.execute(self.controller)

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        pass
