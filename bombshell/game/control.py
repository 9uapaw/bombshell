import abc

import pyautogui


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
        pyautogui.press('.')

    @classmethod
    def cast_spell(cls, key: int):
        pyautogui.press(str(key))
        print('Casted spell {}'.format(key))
