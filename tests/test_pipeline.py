"""Tests for engine.pipeline."""

import unittest
from engine.pipeline import convert  # 根据你实际的函数名调整


class TestPipeline(unittest.TestCase):

    def test_basic_conversion(self):
        """基本文本应能转换为 Markdown。"""
        text = "标题\n\n这是正文内容。"
        result = convert(text)
        self.assertIn("#", result)

    def test_empty_input(self):
        """空输入应返回空字符串或不报错。"""
        result = convert("")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
