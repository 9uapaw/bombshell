import abc

import pyautogui


class CharacterController(metaclass=abc.ABCMeta):

    @classmethod
    def move_forward(cls):
        raise NotImplementedError()

    @classmethod
    def cast_spell(cls, key: int):
        raise NotImplementedError()

    @classmethod
    def turn_left(cls, key_presses: int):
        raise NotImplementedError()

    @classmethod
    def turn_right(cls, key_presses: int):
        raise NotImplementedError()


class BasicController(CharacterController):

    @classmethod
    def move_forward(cls):
        pyautogui.press('.')

    @classmethod
    def cast_spell(cls, key: int):
        pyautogui.press(str(key))
        print('Casted spell {}'.format(key))

    @classmethod
    def turn_left(cls, key_presses: int):
        for i in range(0, key_presses):
            pyautogui.press('a')

    @classmethod
    def turn_right(cls, key_presses: int):
        for i in range(0, key_presses):
            pyautogui.press('d')
