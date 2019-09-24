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
        ['distance'],
        'target_guid'
    ]

    def parse(self, raw: str) -> ExtractedData:
        raw = [r for r in raw.split('\n')]
        clean_data = self._extract_value(raw)

        return ExtractedData(
            player_health=int(clean_data[self.ADDON_DATA_POSITION[0]]),
            player_resource=int(clean_data[self.ADDON_DATA_POSITION[1]]),
            player_position=(float(clean_data[self.ADDON_DATA_POSITION[2]]), float(clean_data[self.ADDON_DATA_POSITION[3]])),
            facing=float(clean_data[self.ADDON_DATA_POSITION[4]]),
            combat=bool(clean_data[self.ADDON_DATA_POSITION[5][0]]),
            casting=CastingState(clean_data[self.ADDON_DATA_POSITION[5][1]]),
            target_health=int(clean_data[self.ADDON_DATA_POSITION[6]]),
            target_distance=DistanceRange(clean_data[self.ADDON_DATA_POSITION[7][0]]),
            target_id=int(str(clean_data[self.ADDON_DATA_POSITION[8]])[:5], 16),
            target_guid=int(str(clean_data[self.ADDON_DATA_POSITION[8]]), 16),
        )

    def _extract_value(self, raw: List[str]) -> Dict[(str, List[float])]:
        clean = [v for v in raw if v]
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
                    val = s
                    res[self.ADDON_DATA_POSITION[pos]] = val
                    pos += 1
            except Exception as e:
                print(e)

        return res
