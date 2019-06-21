from core.data import ExtractedData
from core.position.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character import Character, Resource
from game.control import CharacterController
from game.states.base import BaseState
from game.states.start import StartState


class StateHandler:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage):
        self.character = Character(resource_type=Resource.mana)
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
