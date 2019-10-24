from PIL import Image

from game.position.waypoint import PositionStorage
from game.behavior.behavior import CharacterBehavior
from game.player.character import Character
from game.control.control import CharacterController
from game.target import Target


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: 'BaseState' = None):
        self.controller = controller
        self.behavior = behavior
        self.waypoints = waypoints
        self.persistent_state = {}

    def interpret(self, character: Character, target: Target, screen: Image):
        raise NotImplementedError()

    def transition(self, character: Character, target: Target, screen: Image) -> 'BaseState' or None:
        raise NotImplementedError()

