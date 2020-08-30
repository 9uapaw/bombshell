from typing import Tuple

from PIL.Image import Image

from image.converters.color_wrapper import ColorWrapper
from core.data import ExtractedData
from core.logger import Logger
from image.parsers.ocr import OcrParser


class ImageExtractor:

    def __init__(self, roi: Tuple):
        self.screen_roi_range = roi
        self.parser = OcrParser()
        self._color = ColorWrapper()

    def extract_data_from_screen(self, screen: Image) -> ExtractedData or None:
        raw_data = self._color.image_to_string(self._crop_image(screen))

        data = self.parser.parse(raw_data)
        Logger.debug("Parsed data: {}".format(data))

        return data

    def end(self):
        self._color.end()

    def _crop_image(self, screen: Image) -> Image:
        return screen.crop(self.screen_roi_range)

