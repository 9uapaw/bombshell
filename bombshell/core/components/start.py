import time
import uuid
import cv2
from PIL import Image
import numpy as np

from core.config import Config, GlobalConfig
from core.logger import Logger
from exception.core import ExtractException, RecoverableException, UnrecoverableException, CoreException
from game.behavior.character_behavior import CharacterBehavior
from game.control.control import CharacterController
from game.position.waypoint import PositionStorage
from game.state_handler import StateHandler
from image.extractor import ImageExtractor
from image.screeninterceptor import ScreenInterceptor


class StartComponent:

    def __init__(self, config: Config, controller: CharacterController, extractor: ImageExtractor, interceptor: ScreenInterceptor):
        self.config = config
        self._behavior = CharacterBehavior()
        self._waypoints = PositionStorage()
        self._controller = controller
        self._state_handler = StateHandler(controller, self._behavior, self._waypoints)

        self._extractor = extractor
        self._screen_interceptor = interceptor

        self._extract_error_count = 0
        self._recover_error_count = 0

    def start(self, show_window=False):
        self._waypoints.parse(self.config.waypoint['grind'][0]['waypoints'])
        self._behavior.resolve_profile(GlobalConfig.config.behavior)

        for screen in self._screen_interceptor.capture():
            if show_window:
                self._show_window(screen)

            time_before = time.time()
            try:
                data = self._extractor.extract_data_from_screen(screen)
            except ExtractException as e:
                screen.save(f"errorimages\\{str(uuid.uuid4().hex)}.bmp")
                Logger.error("Error while extracting data from addon. Data extracted: {}", e.partial)
                if self._extract_error_count <= GlobalConfig.config.core.extract_error_threshold:
                    self._extract_error_count += 1
                    continue
                else:
                    self._recover_error_count += 1
                    self._state_handler = StateHandler(self._controller, self._behavior, self._waypoints)
            except RecoverableException as e:
                if self._recover_error_count <= GlobalConfig.config.core.recoverable_error_threshold:
                    self._recover_error_count += 1
                    self._state_handler = StateHandler(self._controller, self._behavior, self._waypoints)
                else:
                    raise UnrecoverableException(str(e))

            delta = time.time() - time_before
            Logger.debug("Elapsed time after extraction: {}".format(delta))
            self._state_handler.update(data, screen)

    def _show_window(self, screen: Image):
        roi = screen.crop((0, 0, 240, 360))
        to_show = np.array(roi)
        cv2.imshow('window', to_show)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            raise CoreException()
