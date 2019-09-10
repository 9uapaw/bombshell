from game.position.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character import Character
from game.control.control import CharacterController
from game.target import Target


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        self.controller = controller
        self.behavior = behavior
        self.waypoints = waypoints

    def interpret(self, character: Character, target: Target):
        raise NotImplementedError()

    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        raise NotImplementedError()

