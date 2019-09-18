from game.control.control import CharacterController


class BehaviorAction:

    def __init__(self, behavior: dict):
        self.behavior = behavior

    def execute(self, controller: CharacterController):
        raise NotImplementedError()


class CastAction(BehaviorAction):

    def execute(self, controller: CharacterController):
        controller.cast_spell(self.behavior['action_value'])


class NullAction(BehaviorAction):

    def execute(self, controller: CharacterController):
        pass
