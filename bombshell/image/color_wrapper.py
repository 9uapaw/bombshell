from PIL import Image


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
        'target_guid'  # THIS IS ACTUALLY 3 COLORS COMBINED
    ]

    def rgb2hex(self, r, g, b, a):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def image_to_string(self, image: Image) -> str:
        pix = list(image.convert('RGBA').getdata())
        hexval = self.rgb2hex(pix[self.xy_threshold+2,self.xy_threshold+2])