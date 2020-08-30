from typing import List, Dict

from core.data import ExtractedData, DistanceRange
from core.logger import Logger
from exception.core import RecoverableException, ExtractException
from game.player.attributes import CastingState, LastAbilityExecution
from image.parsers.base import BaseParser


class OcrParser(BaseParser):

    ADDON_DATA_POSITION = [
        'player_health',
        'player_mana',
        'x',
        'y',
        'facing',
        ['combat', 'casting', 'last_ability', 'inventory', 'has_pet', 'first_resource'],
        'target_health',
        ['distance', 'combat'],
        'target_guid',
        'pet_health',
        'pet_mana'
    ]

    def parse(self, raw: str) -> ExtractedData:
        raw = [r for r in raw.split('\n')]
        Logger.debug("Extracting raw data: {}".format(raw))

        try:
            clean_data = self._extract_value(raw)
            data = ExtractedData(
            player_health=int(clean_data[self.ADDON_DATA_POSITION[0]]),
            player_resource=int(clean_data[self.ADDON_DATA_POSITION[1]]),
            player_position=(float(clean_data[self.ADDON_DATA_POSITION[2]]), -float(clean_data[self.ADDON_DATA_POSITION[3]])),
            facing=float(clean_data[self.ADDON_DATA_POSITION[4]]),
            combat=bool(clean_data[self.ADDON_DATA_POSITION[5][0]]),
            casting=CastingState(clean_data[self.ADDON_DATA_POSITION[5][1]]),
            last_ability=LastAbilityExecution(clean_data[self.ADDON_DATA_POSITION[5][2]]),
            target_health=int(clean_data[self.ADDON_DATA_POSITION[6]]),
            target_distance=DistanceRange(clean_data[self.ADDON_DATA_POSITION[7][0]]),
            target_in_combat=bool(clean_data[self.ADDON_DATA_POSITION[7][1]]),
            target_id=int(str(clean_data[self.ADDON_DATA_POSITION[8]])[:5], 16) if len(clean_data[self.ADDON_DATA_POSITION[8]]) > 2 else int(clean_data[self.ADDON_DATA_POSITION[8]]),
            target_guid=int(str(clean_data[self.ADDON_DATA_POSITION[8]]), 16) if len(clean_data[self.ADDON_DATA_POSITION[8]]) > 2 else int(clean_data[self.ADDON_DATA_POSITION[8]]),
            is_inventory_full=bool(clean_data[self.ADDON_DATA_POSITION[5][3]]),
            player_has_pet=bool(clean_data[self.ADDON_DATA_POSITION[5][4]]),
            player_first_resource_available=bool(clean_data[self.ADDON_DATA_POSITION[5][5]]),
            pet_health=int(clean_data[self.ADDON_DATA_POSITION[9]]),
            pet_mana=int(clean_data[self.ADDON_DATA_POSITION[10]]),
            )

            return data
        except Exception as e:
            raise ExtractException(raw)

    def _extract_value(self, raw: List[str]) -> Dict[(str, List[float])]:
        clean = [v for v in raw if v]
        res = {}
        pos = 0

        for s in clean:
                s = s.replace(" ", "")
                s = s.replace(",", "")
                if not s:
                    continue
                if not isinstance(self.ADDON_DATA_POSITION[pos], str):
                    local_pos = 0
                    for c in s:
                        if local_pos > len(self.ADDON_DATA_POSITION[pos]) - 1:
                            break
                        val = float(c)
                        res[self.ADDON_DATA_POSITION[pos][local_pos]] = val
                        local_pos += 1
                    pos += 1
                else:
                    val = s
                    res[self.ADDON_DATA_POSITION[pos]] = val
                    pos += 1

        return res
