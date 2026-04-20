"""Tests for engine.pipeline."""

import unittest
from engine.pipeline import convert_text


class TestPipeline(unittest.TestCase):

    def test_basic_conversion(self):
        """Basic text should be converted to Markdown."""
        text = "Title\n\nThis is the body content."
        result = convert_text(text)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_heading_detection(self):
        """Short line surrounded by blank lines should become a heading."""
        text = "\nMy Notes\n\nThis is the content."
        result = convert_text(text)
        self.assertIn("##", result)

    def test_ordered_list(self):
        """Ordered list items should be detected."""
        text = "1. Apple\n2. Banana\n3. Orange"
        result = convert_text(text)
        self.assertIn("1.", result)

    def test_empty_input(self):
        """Empty input should return an empty string."""
        result = convert_text("")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
