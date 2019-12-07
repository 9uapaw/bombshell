from core.frame import Frame
from game.states.base import BaseState


class IdleState(BaseState):

    def interpret(self, frame: Frame):
        self.log("Idle state. If you see this often, the state flow is broken.")
