import abc


class CharacterController(metaclass=abc.ABCMeta):

    @classmethod
    def move_forward(cls):
        raise NotImplementedError()

    @classmethod
    def cast_spell(cls, key: int):
        raise NotImplementedError()


class BasicController(CharacterController):

    @classmethod
    def move_forward(cls):
        pass

    @classmethod
    def cast_spell(cls, key: int):
        print('Casted spell {}'.format(key))
