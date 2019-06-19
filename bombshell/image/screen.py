from PIL import ImageGrab, Image
import numpy

import mss


class Screen:

        def __init__(self, screen_size: (int, int, int, int)):
            self.screen_size = (0, 40, 800, 640)

        def capture(self):
            with mss.mss() as image:
                while True:
                    screen = image.grab(self.screen_size)
                    yield Image.fromarray(numpy.array(screen))

