import sys
from typing import Tuple, List, Dict

from PIL.Image import Image
import pytesseract
from core.data import ExtractedData, DistanceRange
from etc.const import ADDON_DATA_POSITION


class ImageExtractor:

    def __init__(self, roi: Tuple):
        self.screen_roi_range = roi

    def extract_data_from_screen(self, screen: Image) -> ExtractedData or None:
        raw_data = pytesseract.image_to_string(self._crop_image(screen))
        split_raw = [r for r in raw_data.split('\n')]
        print(split_raw)

        if not split_raw:
            return

        try:
            extracted_values = self._extract_value(split_raw)
            data = ExtractedData(player_health=extracted_values[ADDON_DATA_POSITION[0]][0],
                                 player_position=(
                                     extracted_values[ADDON_DATA_POSITION[2]][0],
                                     extracted_values[ADDON_DATA_POSITION[3]][0]),
                                 player_resource=extracted_values[ADDON_DATA_POSITION[1]][0],
                                 combat=bool(extracted_values[ADDON_DATA_POSITION[4]][0]),
                                 target_health=extracted_values[ADDON_DATA_POSITION[5]][0],
                                 target_distance=DistanceRange(int(extracted_values.get(ADDON_DATA_POSITION[7], [-1])[0])),
                                 facing=extracted_values[ADDON_DATA_POSITION[6]][0])
        except Exception as e:
            print(e.__class__.__name__, e, file=sys.stderr)
            return

        print(data)
        return data

    def _crop_image(self, screen: Image) -> Image:
        return screen.crop(self.screen_roi_range)

    def _extract_value(self, raw: List[str]) -> Dict[(str, List[float])]:
        clean = ["".join(filter(lambda s: s in "0123456789.", d)) for d in raw if d.replace(' ', '')]
        res = {}
        pos = 0

        for s in clean:
            try:
                val = [float(s)]

                if not val:
                    continue

                res[ADDON_DATA_POSITION[pos]] = val
                pos += 1
            except Exception as e:
                print(e)

        return res
