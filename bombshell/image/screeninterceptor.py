import io
import time

from PIL import ImageGrab, Image
import numpy
import sys
import mss
import os

from core.logger import Logger

path_to_dll = (str(os.path.dirname(os.path.dirname(__file__))) + "/assets/libraries/mss_real_shotter.dll").replace("\\","/")
if sys.platform == 'win32':
    path_to_dll = path_to_dll.replace('/','\\')
    import clr
    clr.AddReference(path_to_dll)

    from mss_real_shotter import mss_real_shotter


class ScreenInterceptor:

        def __init__(self, screen_size: (int, int, int, int)):
            self.screen_size = screen_size
            self.capturing = True

        def capture(self):
            if sys.platform == 'win32':
                while self.capturing:
                    clrBytes = mss_real_shotter.CaptureScreen()
                    yield (Image.open((io.BytesIO(bytearray(clrBytes))))).crop(self.screen_size)
            else:
                with mss.mss() as image:
                    while self.capturing:
                        screen = image.grab(self.screen_size)
                        img = Image.fromarray(numpy.array(screen))
                        yield img

        def stop_capturing(self):
            self.capturing = False

