import sys
from typing import Tuple, List, Dict

from PIL.Image import Image
import pytesseract
from core.data import ExtractedData, DistanceRange
from core.logger import Logger
from etc.const import ADDON_DATA_POSITION
from exception.core import RecoverableException, ExtractException
from game.player.character import LastAbilityExecution
from image.ocr_wrapper import OcrWrapper
from image.parsers.ocr import OcrParser
from image.policies.extract_policy import ExtractPolicy
from image.policies.recover import RecoverPolicy


class ImageExtractor:

    def __init__(self, roi: Tuple, policy: ExtractPolicy=None):
        self.screen_roi_range = roi
        self.policy = policy if policy else RecoverPolicy()
        self.parser = OcrParser()
        self._ocr = OcrWrapper()

    def extract_data_from_screen(self, screen: Image) -> ExtractedData or None:
        raw_data = self._ocr.image_to_string(self._crop_image(screen))

        data = self.parser.parse(raw_data)
        Logger.debug("Parsed data: {}".format(data))

        return data

    def end(self):
        self._ocr.end()

    def _crop_image(self, screen: Image) -> Image:
        return screen.crop(self.screen_roi_range)

