import json
import time

import numpy as np

from cv2 import cv2

from core.config import Config
from core.waypoint import PositionStorage
from game.behavior import CharacterBehavior
from game.character import Character, Resource
from game.control import BasicController
from game.state_handler import StateHandler
from image.extractor import ImageExtractor
from image.screen import Screen


class GameLoop:

    def __init__(self, config: Config=None):
        self.config = config
        self.extractor = ImageExtractor((0, 0, 400, 400))
        self.state = StateHandler(BasicController, CharacterBehavior({"100": {"lt": {1}}}, BasicController), PositionStorage())
        self.screen = Screen((0, 40, 800, 640))

    def start(self):
        time.sleep(5)
        for screen in self.screen.capture():
            print(self.state.character)
            roi = screen.crop((0, 0, 400, 400))
            data = self.extractor.extract_data_from_screen(screen)
            if not data:
                continue
            self.state.update(data)
            screen = np.array(roi)
            cv2.imshow('window', screen)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def record_waypoints(self, path: str):
        time.sleep(5)
        waypoints = {'type': 'circle', 'waypoints': []}
        for screen in self.screen.capture():
            data = self.extractor.extract_data_from_screen(screen)
            waypoints['waypoints'].append(data.player_position)

        with open(path, 'w') as wp:
            json.dump(waypoints, wp)

