import locale
import sys

from PIL import Image
# from pytesseract import pytesseract
locale.setlocale(locale.LC_ALL, 'C')
from tesserocr import PyTessBaseAPI
import tesserocr


class OcrWrapper:

    _OPTIONS = ('tessedit_char_whitelist', '0123456789ABCDEF.-')

    def __init__(self):
        if sys.platform == 'win32':
            self._ocr = PyTessBaseAPI(path="C:\\Program Files\\Tesseract-OCR\\tessdata")
        else:
            self._ocr = PyTessBaseAPI()

        self._ocr.SetVariable(self._OPTIONS[0], self._OPTIONS[1])
        pass

    def image_to_string(self, image: Image) -> str:
        image.format = 'PNG'
        self._ocr.SetImage(image)
        raw_data = self._ocr.GetUTF8Text()
        return raw_data

    def end(self):
        self._ocr.End()
