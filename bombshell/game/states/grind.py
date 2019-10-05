import time

from game.behavior.behavior import CharacterBehavior
from game.control.control import CharacterController
from game.player.character import Character
from game.control.follow import PositionFollower
from game.position.waypoint import PositionStorage
from game.states.base import BaseState
from game.target import Target
import game.states.loot


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.engaged = False
        self.last_pull = None

    def interpret(self, character: Character, target: Target):
        if target.hp > 0 and not self.engaged:
            if character.is_moving:
                self.controller.stop()
                character.switch_moving()

            for action in self.behavior.interpret('pull', character, target):
                action.execute(self.controller)

            self.engaged = True
            self.last_pull = time.time()

        if target.hp == 0:
            self.engaged = False
            self.controller.interact_with_target()

        if self.last_pull and time.time() - self.last_pull > 5 and not character.is_in_combat:
            self.engaged = False

        if not character.is_in_combat and not self.engaged:
            for action in self.behavior.interpret('non_combat', character, target):
                action.execute(self.controller)
            self.waypoint_follower.move(character)
            self.controller.switch_target()
        else:
            for action in self.behavior.interpret('grind', character, target):
                action.execute(self.controller)

    def transition(self, character: Character, target: Target) -> BaseState or None:
        #if (not self.engaged) and (self.last_pull is not None):
        #    return game.states.loot.LootState(controller=self.controller, waypoints=self.waypoints, behavior=self.behavior)
        pass
