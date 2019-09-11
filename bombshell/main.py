import time

from core.game_loop import GameLoop
from game.control.control import BasicController
import pyautogui
from gui.window import run_window


def main():
    pyautogui.PAUSE = 0
    game_loop = GameLoop()
    # game_loop.start({'waypoint': 'waypoints/wp.json'})
    game_loop.record_waypoints('waypoints/wp.json')

if __name__ == '__main__':
    # main()
    run_window()
