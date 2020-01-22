from PIL import Image


class ColorWrapper():

    xy_threshold = 0
    colorpixel_size = 13

    ADDON_DATA_SEQUENCE = [
        ['hp', 'mana'],
        'intx',
        'decx',
        'inty',
        'decy',
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

    def get_target_hp_indicator(self, value):
        if value == 16777215:
            return -1

        return value

    def get_target_guid(self, value):
        if value == 4722366482869645213695:
            return -1

        return value

    def image_to_string(self, image: Image) -> []:
        pixel_information = image.load()
        colors = []
        for x in range(len(self.ADDON_DATA_SEQUENCE)):
            # print(str(x) + " - " + str((x * self.colorpixel_size) + 9) + ":" + str(self.xy_threshold + 10))
            hexval = pixel_information[(x * self.colorpixel_size) + 9, self.xy_threshold + 10]
            colors.append(self.rgb2hex(hexval[0], hexval[1], hexval[2]))

        converted_values = []
        converted_values.append(str(int(colors[0][1:4], 16)) + "\n")
        converted_values.append(str(int(colors[0][4:7], 16)) + "\n")
        converted_values.append(str(float(str(int(colors[1][1:7], 16)) + "." + str(int(colors[2][1:7], 16)))) + "\n")
        converted_values.append(str(float(str(int(colors[3][1:7], 16)) + "." + str(int(colors[4][1:7], 16)))) + "\n")
        converted_values.append(str(int(colors[5][1:7], 16) / 1000000) + "\n")
        converted_values.append( (str(   format((int(colors[6][1:7], 16)), '#08b')      )[2:]) + "\n")
        converted_values.append(str(self.get_target_hp_indicator(int(colors[7][1:7], 16))) + "\n")
        converted_values.append(str(int(colors[8][1:7], 16)) + "\n")

        if str(self.get_target_guid(colors[9][1:7] + colors[10][1:7] + colors[11][1:3])) == 'ffffffffffffff':
            converted_values.append('-1')
        else:
            converted_values.append(
                str(self.get_target_guid(colors[9][1:7] + colors[10][1:7] + colors[11][1:3])) + "\n")

        # converted_values.append(str(int(colors[0][1:4], 16)))
        # converted_values.append(str(int(colors[0][4:7], 16)))
        # converted_values.append(str(float(str(int(colors[1][1:7], 16)) + "." + str(int(colors[2][1:7], 16)))))
        # converted_values.append(str(float(str(int(colors[3][1:7], 16)) + "." + str(int(colors[4][1:7], 16)))))
        # converted_values.append(str(int(colors[5][1:7], 16) / 1000000))
        # converted_values.append((str(bin(int(colors[6][1:7], 16)))[2:]))
        # converted_values.append(str(self.get_target_hp_indicator(int(colors[7][1:7], 16))))
        # converted_values.append(str(int(colors[8][1:7], 16)))
        #
        # if str(self.get_target_guid(colors[9][1:7] + colors[10][1:7] + colors[11][1:3])) == 'ffffffffffffff':
        #     converted_values.append('-1')
        # else:
        #     converted_values.append(
        #         str(self.get_target_guid(colors[9][1:7] + colors[10][1:7] + colors[11][1:3])))


        retval = "".join(converted_values)
        # print(retval)

        return retval

    def end(self):
        pass