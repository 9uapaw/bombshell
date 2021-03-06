from PIL import Image

from core.data import ExtractedData
from core.frame import Frame
from game.position.waypoint import PositionStorage
from game.behavior.character_behavior import CharacterBehavior
from game.player.character import Character, Resource
from game.control.control import CharacterController
from game.states.base import BaseState
from game.states.start import StartState
from game.target import Target


class StateHandler:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage):
        self.character = Character(resource_type=Resource.MANA)
        self.controller = controller
        self.behavior = behavior
        self.state = StartState(self.controller, self.behavior, waypoints)  # type: BaseState
        self.target = Target()

    def update(self, data: ExtractedData, screen: Image):
        self.character.update(data)
        self.target.update(data)
        frame = Frame(self.character, self.target, screen)

        self.state.interpret(frame)

        transition = self.state.transition(frame)
        if transition:
            self.state = transition
