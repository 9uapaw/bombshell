import unittest
from typing import Tuple

from PIL.Image import Image

from image.converters.color_wrapper import ColorWrapper


def hex_to_rgb(h: str, rev: bool = False) -> Tuple[int, int, int]:
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)

    if rev:
        return b, g, r
    else:
        return r, g, b


class FakeRGB:

    def __init__(self, data: list):
        self._data = data

    def __getitem__(self, item: Tuple[int, int]):
        return self._data[item[1]][item[0]]


class FakeImage(Image):

    def __init__(self, rgb_vals: list, px_size: int):
        self.rgbs = rgb_vals
        self.px_size = px_size

    def load(self):
        rgbs = []
        [rgbs.extend((rgb,) * self.px_size) for rgb in self.rgbs]

        return FakeRGB([rgbs] * 20)

    def tostring(self, *args, **kw):
        pass

    def fromstring(self, *args, **kw):
        pass

    def offset(self, xoffset, yoffset=None):
        pass


class TestColorParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = ColorWrapper()

    def test_convert(self):
        hp = 100
        mana = 100
        x = 323.12415
        y = 124.12345
        facing = 4.23151
        player_state = "101010"
        target_hp = 50
        target_state = "100000"
        target_guid1 = "123456"
        target_guid2 = "789abc"
        target_guid3 = "de0000"

        resource_hex = "{:03x}{:03x}".format(hp, mana)
        x_int = "{:06x}".format(int(str(x).split(".")[0]))
        x_dec = "{:06x}".format(int(str(x).split(".")[1]))
        y_int = "{:06x}".format(int(str(y).split(".")[0]))
        y_dec = "{:06x}".format(int(str(y).split(".")[1]))
        facing_hex = "{}{:05x}".format(int(str(facing).split(".")[0]), int(str(facing).split(".")[1]))
        target_hp_hex = "{:06x}".format(target_hp)

        hex_vals = [resource_hex, x_int, x_dec, y_int, y_dec, facing_hex, player_state, target_hp_hex, target_state, target_guid1, target_guid2, target_guid3]
        rgb_vals = [hex_to_rgb(h, True) for h in hex_vals]

        image = FakeImage(rgb_vals, 15)

        res = self.parser.image_to_string(image).split("\n")

        self.assertEqual(str(hp), res[0])
        self.assertEqual(str(mana), res[1])
        self.assertEqual(str(x), res[2])
        self.assertEqual(str(y), res[3])
        self.assertEqual(str(facing), res[4])
        self.assertEqual(str(player_state), res[5])
        self.assertEqual(str(target_hp), res[6])
        self.assertEqual(str(target_state), res[7])
        self.assertEqual(str(target_guid1+target_guid2+target_guid3[:2]), res[8])


