import pyautogui

from core.game_loop import GameLoop


def main():
    game_loop = GameLoop()
    game_loop.start({'waypoint': 'waypoints/wp.json'})
    # game_loop.record_waypoints('waypoints/wp.json')

main()