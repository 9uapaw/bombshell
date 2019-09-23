from PIL import ImageGrab, Image
import numpy

import mss


class Screen:

        def __init__(self, screen_size: (int, int, int, int)):
            self.screen_size = screen_size
            self.capturing = True

        def capture(self):
            with mss.mss() as image:
                while self.capturing:
                    screen = image.grab(self.screen_size)
                    yield Image.fromarray(numpy.array(screen))

        def stop_capturing(self):
            self.capturing = False

