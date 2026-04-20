"""Tests for engine.lang."""

import unittest
from engine.lang import detect  # 根据你实际的函数名调整


class TestLang(unittest.TestCase):

    def test_chinese(self):
        result = detect("这是中文文本")
        self.assertEqual(result, "zh")

    def test_english(self):
        result = detect("This is English text")
        self.assertEqual(result, "en")

    def test_empty(self):
        result = detect("")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
