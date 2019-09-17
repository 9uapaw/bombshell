import abc
from typing import Tuple

import pyautogui

class CharacterController(metaclass=abc.ABCMeta):

    @classmethod
    def move_forward(cls):
        raise NotImplementedError()

    @classmethod
    def stop(cls):
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

    @classmethod
    def switch_target(cls):
        raise NotImplementedError()


class BasicController(CharacterController):

    @classmethod
    def move_forward(cls):
        pyautogui.press('.')

    @classmethod
    def stop(cls):
        pyautogui.press('.')

    @classmethod
    def cast_spell(cls, key: int):
        pyautogui.press(str(key))
        print('Casted spell {}'.format(key))

    @classmethod
    def switch_target(cls):
        pyautogui.press('tab')

    @classmethod
    def turn_left(cls, key_presses: int):
        for i in range(0, key_presses):
            pyautogui.press('a')

    @classmethod
    def turn_right(cls, key_presses: int):
        for i in range(0, key_presses):
            pyautogui.press('d')

    @classmethod
    def click_in_middle(cls, area: Tuple[Tuple[int, int],Tuple[int, int],Tuple[int, int],Tuple[int, int]]):
        pyautogui.click((area[0][0]+area[1][0])/2, (area[0][1]+area[2][1])/2)
