from typing import Dict

from core.data import ExtractedData


class ExtractPolicy:

    def set_history(self, data: Dict[str, str]):
        raise NotImplementedError()

    def decide(self, unit: str):
        raise NotImplementedError()

    def rollback(self, partial_data: Dict[str, str]) -> Dict[str, str]:
        raise NotImplementedError()
