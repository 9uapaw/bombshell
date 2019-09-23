import unittest

from image.parsers.ocr import OcrParser


class TestOcrParser(unittest.TestCase):

    def setUp(self):
        self.parser = OcrParser()

    def test_parse_states(self):
        combat_state = '1'
        casting_state = '1'
        target_distance_state = '2'
        raw = "86\n55\n56.23123\n52.1233\n5.232323\n{}\n56\n{}".format(combat_state + casting_state, target_distance_state)

        data = self.parser.parse(raw)

        self.assertEqual(data.combat, int(combat_state))
        self.assertEqual(data.casting.value, int(casting_state))
        self.assertEqual(data.target_distance.value, int(target_distance_state))