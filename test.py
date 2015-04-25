import re
import unittest

from app import TEMP_REGEX
from app import convert_temp


class TemperatureTest(unittest.TestCase):

    def test_regex(self):
        phrases = [
            ('set temperature sixty degrees', 60),
            ('set the temperature sixty degrees', 60),
            ('set temperature to sixty degrees', 60),
            ('set the temperature to sixty degrees', 60),
            ('temperature sixty degrees', 60),
            ('sixty degrees', 60),
        ]

        temp_regex = re.compile(TEMP_REGEX)
        for phrase, expected in phrases:
            m = temp_regex.match(phrase)
            self.assertEqual(convert_temp(m), expected)
