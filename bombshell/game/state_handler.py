from core.data import ExtractedData
from game.position.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character.character import Character, Resource
from game.control.control import CharacterController
from game.states.base import BaseState
from game.states.start import StartState


class StateHandler:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage):
        self.character = Character(resource_type=Resource.MANA)
        self.controller = controller
        self.behavior = behavior
        self.state = StartState(self.controller, self.behavior, waypoints)  # type: BaseState
        self.target = None

    def update(self, data: ExtractedData):
        self.character.update(data)
        self.state.interpret(self.character, self.target)

        transition = self.state.transition(self.character, self.target)
        if transition:
            self.state = transition
