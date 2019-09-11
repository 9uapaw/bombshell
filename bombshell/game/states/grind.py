from game.character.character import Character
from game.control.follow import PositionFollower
from game.states.base import BaseState
from game.target import Target


class GrindState(BaseState):

    def __init__(self, controller: CharacterController, behavior: CharacterBehavior, waypoints: PositionStorage = None):
        super().__init__(controller, behavior, waypoints)
        self.waypoint_follower = PositionFollower(self.controller, self.waypoints)
        self.tab

    def interpret(self, character: Character, target: Target):


    def transition(self, character: Character, target: Target) -> 'BaseState' or None:
        pass