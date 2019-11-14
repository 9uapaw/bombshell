from PIL import Image

from core.logger import Logger
from game.position.waypoint import PositionStorage
from game.behavior.character_behavior import CharacterBehavior
from game.player.character import Character
from game.control.control import CharacterController
from game.target import Target


class BaseState:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None, previous_state: 'BaseState' = None):
        Logger.info("Initiating {}".format(self.__class__.__name__))
        self.controller = controller
        self.behavior = behavior
        self.waypoints = waypoints
        self.persistent_state = {}

    def interpret(self, character: Character, target: Target, screen: Image = None):
        raise NotImplementedError()

    def transition(self, character: Character, target: Target, screen: Image = None) -> 'BaseState' or None:
        raise NotImplementedError()

