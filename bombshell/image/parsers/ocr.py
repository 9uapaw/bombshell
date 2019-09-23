from typing import List, Dict

from core.data import ExtractedData, DistanceRange
from game.player.attributes import CastingState
from image.parsers.base import BaseParser


class OcrParser(BaseParser):

    ADDON_DATA_POSITION = [
        'player_health',
        'player_mana',
        'x',
        'y',
        'facing',
        ['combat', 'casting'],
        'target_health',
        ['distance']
    ]

    def parse(self, raw: str) -> ExtractedData:
        raw = [r for r in raw.split('\n')]
        clean_data = self._extract_value(raw)

        return ExtractedData(
            player_health=clean_data[self.ADDON_DATA_POSITION[0]],
            player_resource=clean_data[self.ADDON_DATA_POSITION[1]],
            player_position=(clean_data[self.ADDON_DATA_POSITION[2]], clean_data[self.ADDON_DATA_POSITION[3]]),
            facing=clean_data[self.ADDON_DATA_POSITION[4]],
            combat=clean_data[self.ADDON_DATA_POSITION[5][0]],
            casting=CastingState(clean_data[self.ADDON_DATA_POSITION[5][1]]),
            target_health=clean_data[self.ADDON_DATA_POSITION[6]],
            target_distance=DistanceRange(clean_data[self.ADDON_DATA_POSITION[7][0]])
        )

    def _extract_value(self, raw: List[str]) -> Dict[(str, List[float])]:
        clean = ["".join(filter(lambda s: s in "0123456789.-", d)) for d in raw if d.replace(' ', '')]
        res = {}
        pos = 0

        for s in clean:
            try:
                if not s:
                    continue
                if not isinstance(self.ADDON_DATA_POSITION[pos], str):
                    local_pos = 0
                    for c in s:
                        val = float(c)
                        res[self.ADDON_DATA_POSITION[pos][local_pos]] = val
                        local_pos += 1
                    pos += 1
                else:
                    val = float(s)
                    res[self.ADDON_DATA_POSITION[pos]] = val
                    pos += 1
            except Exception as e:
                print(e)

        return res
