"""Tests for engine.lang."""

import unittest
from engine.lang import detect


class TestLang(unittest.TestCase):

    def test_chinese(self):
        result = detect("This is a Chinese text test")
        self.assertIsInstance(result, str)

    def test_english(self):
        result = detect("This is an English sentence")
        self.assertEqual(result, "en")

    def test_empty(self):
        result = detect("")
        self.assertEqual(result, "unknown")


if __name__ == "__main__":
    unittest.main()
