from PIL import ImageGrab, Image


class Screen:

        def __init__(self, screen_size: (int, int, int, int)):
            self.screen_size = (0, 40, 800, 640)

        def capture(self):
            while True:
                screen = ImageGrab.grab(bbox=self.screen_size)
                yield screen

