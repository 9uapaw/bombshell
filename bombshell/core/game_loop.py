import datetime
import json
import sys
import time
import traceback
from typing import Dict

import numpy as np
from PIL import Image

from cv2 import cv2

from core.config import Config
from core.logger import Logger
from game.position.waypoint import PositionStorage
from exception.base import BombShellException
from exception.core import CoreException
from game.behavior.behavior import CharacterBehavior
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

        time_before = datetime.datetime.now()
        try:
            for screen in self.screen.capture():
                # self._show_window(screen)
                delta = datetime.datetime.now() - time_before
                data = self.extractor.extract_data_from_screen(screen)
                Logger.debug("Elapsed time after extraction: {}".format(delta.total_seconds() * 1000))
                time_before = datetime.datetime.now()
                if not data:
                    continue
                self.state.update(data)

        except BombShellException as e:
            Logger.error("{}".format(e), output=True)
            self.screen.stop_capturing()
            return
        except Exception as e:
            Logger.error(traceback.format_exc(), output=True)
            self.screen.stop_capturing()
        finally:
            self.extractor.end()

    def record_waypoints(self, paths: Dict[str, str]):
        waypoints = {'format': paths['wp_format'], 'waypoints': []}
        for screen in self.screen.capture():
            data = self.extractor.extract_data_from_screen(screen)
            print('Recording position: ', data.player_position)
            waypoints['waypoints'].append(data.player_position)
            time.sleep(2)

        print('Saving file to: ', paths.get('waypoint', 'NO PATH'))
        with open(paths['waypoint'], 'w') as wp:
            file = json.load(wp)
            file[paths['wp_type']] = waypoints
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
        self.waypoints.parse(wp['grind']['waypoints'])

