import time

import pyautogui
from PIL import Image
from cv2 import cv2

from core.config import GlobalConfig
from exception.core import CoreException
from image.converters.color_wrapper import ColorWrapper
from image.screeninterceptor import ScreenInterceptor

import numpy as np

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
        time.sleep(0.1)
        rgb_im = screen.convert('RGB')
        print(parser.image_to_string(screen))
        print('*'*30)
        # _show_window(screen)


