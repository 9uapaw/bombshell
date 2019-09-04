import datetime
import json
import sys
import time
from typing import Dict

import numpy as np
from PIL import Image

from cv2 import cv2

from core.config import Config
from core.position.waypoint import PositionStorage
from exception.base import BombShellException
from exception.core import CoreException
from game.behavior import CharacterBehavior
from game.control import BasicController
from game.state_handler import StateHandler
from image.extractor import ImageExtractor
from image.screen import Screen


class GameLoop:

    def __init__(self, config: Config=None):
        self.config = config if config else Config()
        self.extractor = ImageExtractor(self.config.roi)
        self.waypoints = PositionStorage()
        self.controller = BasicController
        self.state = StateHandler(self.controller, CharacterBehavior({"100": {"lt": {1}}}, self.controller), self.waypoints)
        self.screen = Screen(self.config.screen_res)

    def start(self, paths: Dict[str, str]):
        self._parse_waypoints(paths['waypoint'])

        # time.sleep(5)
        time_before = datetime.datetime.now()
        try:
            for screen in self.screen.capture():
                # self._show_window(screen)
                # delta = datetime.datetime.now() - time_before
                # print(self.state.character)
                data = self.extractor.extract_data_from_screen(screen)
                # print(delta.total_seconds() * 1000)
                # time_before = datetime.datetime.now()
                if not data:
                    continue
                self.state.update(data)
        except BombShellException as e:
            print(e, file=sys.stderr)

    def record_waypoints(self, paths: Dict[str, str]):
        # time.sleep(5)
        waypoints = {'type': 'circle', 'waypoints': []}
        for screen in self.screen.capture():
            data = self.extractor.extract_data_from_screen(screen)
            print('Recording position: ', data.player_position)
            waypoints['waypoints'].append(data.player_position)
            time.sleep(2)

        print('Saving file to: ', paths.get('waypoint', 'NO PATH'))
        with open(paths['waypoint'], 'w') as wp:
            json.dump(waypoints, wp)

    def _show_window(self, screen: Image):
        roi = screen.crop((0, 0, 240, 360))
        to_show = np.array(roi)
        cv2.imshow('window', to_show)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise CoreException()

    def _parse_waypoints(self, path: str) -> dict:
        with open(path) as wp_file:
            wp = json.load(wp_file)
            self.waypoints.parse(wp['waypoints'])

