from core.data import ExtractedData
from core.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character import Character, Resource
from game.control import CharacterController
from game.states.base import BaseState
from game.states.move import MoveState
from game.target import Target


class StateHandler:

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage):
        self.character = Character(resource_type=Resource.mana)
        self.controller = controller
        self.behavior = behavior
        self.state = MoveState(self.controller, self.behavior)  # type: BaseState
        self.target = None

    def update(self, data: ExtractedData):
        self.character.update(data)
        self.state.interpret(self.character, self.target)

        transition = self.state.transition()
        if transition:
            self.state = transition
