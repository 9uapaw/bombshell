import time

import numpy as np
from PIL import Image
from core.config import GlobalConfig
from cv2 import cv2

from core.frame import Frame
from exception.core import CoreException
from game.control.control import BasicController
from game.states.loot import LootState
from image.converters.color_wrapper import ColorWrapper
from image.screeninterceptor import ScreenInterceptor

extractor = ScreenInterceptor(GlobalConfig.config.screen_res)
parser = ColorWrapper()
time.sleep(5)


def _show_window(screen: Image):
    roi = screen.crop((0, 0, 240, 360))
    to_show = np.array(roi)
    cv2.imshow('window', to_show)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        raise CoreException()


if __name__ == '__main__':
    for screen in extractor.capture():
        # loot = LootState(BasicController(), None)
        # loot.interpret(Frame(None, None, screen))
        time.sleep(2)
        rgb_im = screen.convert('RGB')
        print(parser.image_to_string(screen))
        print('*'*30)
        # _show_window(screen)


