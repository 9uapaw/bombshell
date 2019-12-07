import json
import signal
import time
import traceback
from pathlib import Path
from typing import Dict

from core.components.record import RecordComponent
from core.components.start import StartComponent
from core.config import Config, GlobalConfig
from core.logger import Logger
from game.position.waypoint import PositionStorage
from exception.base import BombShellException
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import BasicController
from game.state_handler import StateHandler
from image.extractor import ImageExtractor
from image.screeninterceptor import ScreenInterceptor


class GameLoop:

    def __init__(self, config: Config):
        self.extractor = ImageExtractor(GlobalConfig.config.roi)
        self.waypoints = PositionStorage()
        self.controller = BasicController

        self.behavior = CharacterBehavior()

        self.state = None
        self.screen = ScreenInterceptor(GlobalConfig.config.screen_res)

    def start(self):
        try:
            start = StartComponent(GlobalConfig.config, self.controller, self.extractor, self.screen)
            start.start()
        except BombShellException as e:
            Logger.error("Exiting with a handled error: {}".format(e))
        except Exception as e:
            Logger.error("Unexpected error")
            Logger.error(traceback.format_exc())
        finally:
            self.screen.stop_capturing()
            self.extractor.end()

    def record_waypoints(self, paths: Dict[str, str]):
        record = RecordComponent(self.controller, self.extractor, self.screen)
        record.record(paths)
