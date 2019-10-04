import abc
import time
from typing import Tuple

import pyautogui
import pynput
from pynput.keyboard import Controller

from core.logger import Logger


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
    def turn_left(cls, press_time: float):
        raise NotImplementedError()

    @classmethod
    def turn_right(cls, press_time: float):
        raise NotImplementedError()

    @classmethod
    def switch_target(cls):
        raise NotImplementedError()

    @classmethod
    def interact_with_target(cls):
        raise NotImplementedError()

    @classmethod
    def right_click(cls):
        raise NotImplementedError()

    @classmethod
    def move_mouse(cls, x: int, y: int):
        raise NotImplementedError()


class BasicController(CharacterController):

    @classmethod
    def interact_with_target(cls):
        pyautogui.press('t')

    @classmethod
    def move_forward(cls):
        pyautogui.keyDown('w')
        # pyautogui.press('.')

    @classmethod
    def stop(cls):
        pyautogui.keyUp('w')
        # pyautogui.press('[')

    @classmethod
    def cast_spell(cls, key: int):
        pyautogui.press(str(key))

    @classmethod
    def switch_target(cls):
        pyautogui.press('tab')

    # @classmethod
    # def turn_left(cls, key_presses: int):
    #     for i in range(0, key_presses):
    #         pyautogui.press('a')
    #
    # @classmethod
    # def turn_right(cls, key_presses: int):
    #     for i in range(0, key_presses):
    #         pyautogui.press('d')

    @classmethod
    def turn_left(cls, press_time: float):
        Logger.debug("Sleep time: {}".format(press_time))
        now = time.time()
        pyautogui.keyDown('a')
        while time.time() - now <= press_time:
            pass
        pyautogui.keyUp('a')

    @classmethod
    def turn_right(cls, press_time: float):
        Logger.debug("Sleep time: {}".format(press_time))
        now = time.time()
        pyautogui.keyDown('d')
        while time.time() - now <= press_time:
            pass
        pyautogui.keyUp('d')

    @classmethod
    def click_in_middle(cls, area: Tuple[Tuple[int, int],Tuple[int, int],Tuple[int, int],Tuple[int, int]]):
        pyautogui.click((area[0][0]+area[1][0])/2, (area[0][1]+area[2][1])/2)

    @classmethod
    def right_click(cls):
        pyautogui.click(button='right')

    @classmethod
    def move_mouse(cls, x: int, y: int):
        pyautogui.moveTo(x, y)
