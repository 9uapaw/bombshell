import time
from concurrent.futures import thread

import numpy as np

from PIL import ImageGrab
from cv2 import cv2
import pyautogui
from pynput.mouse import Controller, Listener

from core.config import Config
from game.behavior import CharacterBehavior
from game.character import Character, Resource
from game.control import BasicController
from game.state_handler import StateHandler
from image.extractor import ImageExtractor


class GameLoop:

    def __init__(self, config: Config=None):
        self.config = config
        self.extractor = ImageExtractor((0, 0, 400, 400))
        self.character = Character(resource_type=Resource.mana)
        self.state = StateHandler(self.character, BasicController, CharacterBehavior({"100": {"lt": {1}}}, BasicController))

    def start(self):
        time.sleep(5)
        while True:
            print(self.state.character)
            screen = ImageGrab.grab(bbox=(0, 40, 800, 640))
            roi = screen.crop((0, 0, 400, 400))
            data = self.extractor.extract_data_from_screen(screen)
            self.state.update(data)
            screen = np.array(roi)
            cv2.imshow('window', screen)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break