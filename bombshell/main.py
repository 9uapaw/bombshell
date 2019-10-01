import logging
import sys
import pyautogui

from gui.window import run_window


if __name__ == '__main__':
    pyautogui.PAUSE = 0
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    run_window()
