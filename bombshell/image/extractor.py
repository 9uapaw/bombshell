from typing import Tuple

from PIL.Image import Image
import pytesseract
from core.data import ExtractedData


class ImageExtractor:

    def __init__(self, roi: Tuple):
        self.screen_roi_range = roi

    def extract_data_from_screen(self, screen: Image) -> ExtractedData:
        raw_data = pytesseract.image_to_string(self._crop_image(screen))
        split_raw = [r for r in raw_data.split('\n')]
        health = 95 if 'HEALTH' in split_raw[0] else 0
        data = ExtractedData(player_health=health, player_position=raw_data, target_health=40)

        print(data)
        return data

    def _crop_image(self, screen: Image) -> Image:
        return screen.crop(self.screen_roi_range)
