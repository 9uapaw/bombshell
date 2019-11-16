import datetime
import json
import signal
import sys
import time
import traceback
from pathlib import Path
from typing import Dict

import numpy as np
from PIL import Image

from cv2 import cv2

from core.config import Config
from core.logger import Logger
from game.position.waypoint import PositionStorage
from exception.base import BombShellException
from exception.core import CoreException
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import BasicController
from game.state_handler import StateHandler
from image.extractor import ImageExtractor
from image.screen import Screen


class GameLoop:

    def __init__(self, config: Config):
        self.config = config
        self.extractor = ImageExtractor(self.config.roi)
        self.waypoints = PositionStorage()
        self.controller = BasicController

        self.behavior = CharacterBehavior()

        self.state = None
        self.screen = Screen(self.config.screen_res)

    def start(self):
        self.state = StateHandler(self.controller, self.behavior, self.waypoints)

        self.behavior.resolve_profile(self.config.behavior)
        self._parse_waypoints()
        time.sleep(3)

        try:
            for screen in self.screen.capture():
                # self._show_window(screen)
                time_before = time.time()
                data = self.extractor.extract_data_from_screen(screen)
                delta = time.time() - time_before
                Logger.debug("Elapsed time after extraction: {}".format(delta))
                if not data:
                    continue
                self.state.update(data, screen)

        except BombShellException as e:
            Logger.error("{}".format(e))
            self.screen.stop_capturing()
            return
        except Exception as e:
            Logger.error(traceback.format_exc())
            self.screen.stop_capturing()
        finally:
            self.extractor.end()

    def record_waypoints(self, paths: Dict[str, str]):
        waypoints = {'format': paths['wp_format'], 'waypoints': []}

        signal.signal(signal.SIGINT, lambda *args: self.screen.stop_capturing())
        signal.signal(signal.SIGTERM, lambda *args: self.screen.stop_capturing())

        try:
            for screen in self.screen.capture():
                data = self.extractor.extract_data_from_screen(screen)
                Logger.info('Recording position: ' + str(data.player_position))
                waypoints['waypoints'].append(data.player_position)
                time.sleep(2)

            Logger.info('Saving file to: {}'.format(paths.get('waypoint', 'NO PATH')))
        finally:
            file = Path(paths['waypoint'])
            if file.is_file():
                with open(paths['waypoint'], 'r+') as wp:
                    file = json.load(wp)
                    if paths['wp_type'] in file:
                        file[paths['wp_type']].append(waypoints)
                    else:
                        file[paths['wp_type']] = [waypoints]
                    wp.seek(0)
                    json.dump(file, wp)
            else:
                with open(paths['waypoint'], 'w+') as wp:
                    file = {paths['wp_type']: []}
                    file[paths['wp_type']].append(waypoints)
                    json.dump(file, wp)

    def _show_window(self, screen: Image):
        roi = screen.crop((0, 0, 240, 360))
        to_show = np.array(roi)
        cv2.imshow('window', to_show)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise CoreException()

    def _parse_waypoints(self):
        wp = self.config.waypoint
        self.waypoints.parse(wp['grind'][0]['waypoints'])

