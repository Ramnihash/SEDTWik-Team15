
import unittest

from preprocessing.text_processor import clean_text, tokenize, extract_hashtags


class TestTextProcessor(unittest.TestCase):
    def test_converts_text_to_lowercase(self):
        self.assertEqual(clean_text("BOSTON MARATHON"), "boston marathon")

    def test_removes_urls(self):
        result = clean_text("Breaking news https://example.com")

        self.assertNotIn("https://example.com", result)
        self.assertNotIn("example.com", result)

    def test_removes_mentions(self):
        result = clean_text("Hello @news team")

        self.assertNotIn("@news", result)
        self.assertIn("hello", result)
        self.assertIn("team", result)

    def test_preserves_hashtags(self):
        result = clean_text("Breaking News #NobelPrize")

        self.assertIn("#nobelprize", result)

    def test_tokenize_splits_cleaned_text(self):
        self.assertEqual(
            tokenize("Hello, WORLD!"),
            ["hello", "world"]
        )

    def test_extracts_multiple_hashtags(self):
        self.assertEqual(
            extract_hashtags("Today #NobelPrize and #BostonStrong"),
            ["#nobelprize", "#bostonstrong"]
        )

    def test_empty_text(self):
        self.assertEqual(clean_text(""), "")
        self.assertEqual(tokenize(""), [])
        self.assertEqual(extract_hashtags(""), [])

    def test_handles_none_input(self):
        self.assertEqual(clean_text(None), "none")


if __name__ == "__main__":
    unittest.main()
