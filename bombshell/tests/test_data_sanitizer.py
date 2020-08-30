import unittest

from core.data import ExtractedData
from core.data_sanitizer import DataSanitizer


class TestDataSanitizer(unittest.TestCase):

    def test_coord_sanitizer(self):
        sanitizer = DataSanitizer()
        datas = []
        last_y = 0
        for i in range(700, 730, 3):
            datas.append(ExtractedData(0, 0, (i, i - 700 + 50), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, False, False))
            last_y = i - 700 + 50

        [sanitizer.sanitize_data(data) for data in datas]
        outlier = ExtractedData(0, 0, (11000, last_y + 3), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, False, False, False, False)
        self.assertEqual(outlier.player_position[0], 11000)
        sanitizer.sanitize_data(outlier)
        self.assertEqual(outlier.player_position[0], 730)

if __name__ == '__main__':
    unittest.main()
