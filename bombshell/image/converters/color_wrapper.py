from typing import List

from PIL import Image

from image.converters.base import BaseImageToString


class ColorWrapper(BaseImageToString):

    Y_THRESHOLD = 10
    COLORPIXEL_SIZE = 28
    X_THRESHOLD = 5

    ADDON_DATA_SEQUENCE = [
        ['hp', 'mana'],
        'intx',
        'decx',
        'inty',
        'decy',
        'facing',
        ['combat', 'casting', 'last_ability', 'inventory', 'has_pet', 'first_resource'],
        'target_health',
        ['distance', 'combat'],
        'target_guid1',
        'target_guid2',
        'target_guid3',
        'pet_resource'
        # THIS IS ACTUALLY 3 COLORS COMBINED
    ]

    def image_to_string(self, image: Image) -> []:
        pixel_information = image.load()
        colors = []
        for x in range(len(self.ADDON_DATA_SEQUENCE)):
            hexval = pixel_information[(x * self.COLORPIXEL_SIZE) + self.X_THRESHOLD, self.Y_THRESHOLD]
            color = self._rgb2hex(hexval[2], hexval[1], hexval[0])
            colors.append(color)

        converted_values = [
            self._to_hp_mana(colors),
            self._to_x_y(colors),
            self._to_facing(colors),
            self._to_state(colors, 6),
            self._to_target_hp(colors),
            self._to_state(colors, 8),
            self._to_target_guid(colors),
            self._to_hp_mana(colors, 12),
        ]

        res = "".join(converted_values)

        return res

    @staticmethod
    def _to_hp_mana(colors: List[str], i: int = 0) -> str:
        hex_val = colors[i]

        return "{}\n{}\n".format(str(int(hex_val[1:4], 16)), str(int(hex_val[4:7], 16)))

    @staticmethod
    def _to_x_y(colors: List[str]) -> str:
        x_int = colors[1]
        x_dec = colors[2]
        y_int = colors[3]
        y_dec = colors[4]

        x = (str(float(str(int(x_int[1:7], 16)) + "." + str(int(x_dec[1:7], 16)))) + "\n")
        y = (str(float(str(int(y_int[1:7], 16)) + "." + str(int(y_dec[1:7], 16)))) + "\n")

        return x+y

    @staticmethod
    def _to_facing(colors: List[str]) -> str:
        hex_val = colors[5]
        return hex_val[1] + '.' + str(int(hex_val[2:], 16)) + "\n"

    @staticmethod
    def _to_state(colors: List[str], i: int) -> str:
        return colors[i][1:7] + "\n"

    @staticmethod
    def _to_target_hp(colors: List[str]) -> str:
        hp = colors[7][1:7]

        if hp == "ffffff":
            val = "-1"
        else:
            val = str(int(hp, 16))

        return val + "\n"

    @staticmethod
    def _to_target_guid(colors: List[str]) -> str:
        guid = colors[9][1:7] + colors[10][1:7] + colors[11][1:3]

        if guid == "ffffffffffffff":
            return "-1" "\n"
        else:
            return guid + "\n"

    @staticmethod
    def _rgb2hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
