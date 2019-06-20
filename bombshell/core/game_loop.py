import datetime
import json
import sys
import time

import numpy as np

from cv2 import cv2

from core.config import Config
from core.position.waypoint import PositionStorage
from exception.base import BombShellException
from game.behavior import CharacterBehavior
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
        time_before = datetime.datetime.now()
        try:
            for screen in self.screen.capture():
                delta = datetime.datetime.now() - time_before
                print(self.state.character)
                roi = screen.crop((0, 0, 400, 400))
                screen = np.array(roi)
                cv2.imshow('window', screen)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
                data = self.extractor.extract_data_from_screen(screen)
                print(delta.total_seconds() * 1000)
                time_before = datetime.datetime.now()
                if not data:
                    continue
                self.state.update(data)
        except BombShellException as e:
            print(e, file=sys.stderr)

    def record_waypoints(self, path: str):
        time.sleep(5)
        waypoints = {'type': 'circle', 'waypoints': []}
        i = 0
        for screen in self.screen.capture():
            data = self.extractor.extract_data_from_screen(screen)
            waypoints['waypoints'].append(data.player_position)
            time.sleep(2)
            i += 1
            if i == 10:
                break

        with open(path, 'w') as wp:
            json.dump(waypoints, wp)

