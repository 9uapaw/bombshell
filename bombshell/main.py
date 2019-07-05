import pyautogui

from core.game_loop import GameLoop
from gui.window import run_window


def main():
    game_loop = GameLoop()
    game_loop.start({'waypoint': 'waypoints/wp.json'})
    # game_loop.record_waypoints('waypoints/wp.json')


if __name__ == '__main__':
    # main()
    run_window()
