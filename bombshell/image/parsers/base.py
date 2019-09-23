from typing import List, Dict

from core.data import ExtractedData


class BaseParser:

    def parse(self, raw: str) -> ExtractedData:
        raise NotImplementedError()