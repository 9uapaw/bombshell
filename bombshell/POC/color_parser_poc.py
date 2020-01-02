from PIL import Image
import time


class ColorWrapper():

    xy_threshold = 5
    colorpixel_size = 5

    ADDON_DATA_SEQUENCE = [
        ['hp', 'mana'],
        'x',
        'y',
        'coord_divider_position',
        'facing',
        ['combat', 'casting', 'last_ability', 'inventory', 'has_pet', 'first_resource'],
        'target_health',
        ['distance'],
        'target_guid1',
        'target_guid2',
        'target_guid3'
        # THIS IS ACTUALLY 3 COLORS COMBINED
    ]

    def rgb2hex(self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def get_range_indicator(self, value):
        if value == 16777215:
            return -1

        return value

    def get_target_guid(self, value):
        if value == 'ffffffffffffff':
            return -1

        return value

    def image_to_string(self, image: Image) -> []:
        pixel_information = image.load()
        colors = []
        print(len(self.ADDON_DATA_SEQUENCE))
        for x in range(len(self.ADDON_DATA_SEQUENCE)):
            hexval = pixel_information[self.xy_threshold + (x * self.colorpixel_size) + 2, self.xy_threshold + 2]
            colors.append(self.rgb2hex(hexval[0], hexval[1], hexval[2]))

        converted_values = []
        converted_values.append(str(int(colors[0][1:4], 16)))
        converted_values.append(str(int(colors[0][4:7], 16)))
        converted_values.append(int(colors[1][1:7], 16))
        converted_values.append(int(colors[2][1:7], 16))
        converted_values[2] = converted_values[2] / (pow(10, 7 - int(colors[3][3])))
        converted_values[3] = converted_values[3] / (pow(10, 7 - int(colors[3][6])))
        converted_values[2] = str(converted_values[2])
        converted_values[3] = str(converted_values[3])
        converted_values.append(str(int(colors[4][1:7], 16) / 1000000))
        converted_values.append(str(int(colors[5][1:7], 16)))
        converted_values.append(str(self.get_range_indicator(int(colors[6][1:7], 16))))
        converted_values.append(str(int(colors[7][1:7], 16)))
        converted_values.append(str(self.get_target_guid(colors[8][1:7] + colors[9][1:7] + colors[10][1:3])))
        return converted_values



img = Image.open('C:\\Users\\Andris\\PycharmProjects\\bombshell_new\\bombshell\\MOCKED_COLOR_DATA_target_guid_0.png')
clrwrapper = ColorWrapper()
start_time = time.time()
ret = clrwrapper.image_to_string(img)
endtime = time.time()
print(ret)
print("--- %s seconds ---" % (endtime - start_time))