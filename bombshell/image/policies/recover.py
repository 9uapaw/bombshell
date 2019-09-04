from typing import Dict

from core.data import ExtractedData
from etc.const import ADDON_DATA_POSITION
from exception.core import ExtractException, RecoverableException
from image.policies.extract_policy import ExtractPolicy


class RecoverPolicy(ExtractPolicy):
    ROLLBACK_ON = ["HEALTH", "THP"]

    def __init__(self):
        self.data = {}

    def set_history(self, data: Dict[str, str]):
        self.data = data

    def decide(self, unit: str, partial: dict):
        if unit in self.ROLLBACK_ON:
            raise ExtractException(partial)
        else:
            raise RecoverableException()

    def rollback(self, partial_data: Dict[str, str]) -> Dict[str, str]:
        for unit in ADDON_DATA_POSITION:
            if unit.lower() not in partial_data:
                partial_data[unit.lower()] = self.data[unit.lower()]

        return partial_data
