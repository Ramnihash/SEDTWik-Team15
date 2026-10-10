
import unittest

from segmentation.segmenter import segment_tweet


class TestTweetSegmentation(unittest.TestCase):
    def test_extracts_meaningful_phrases(self):
        segments = segment_tweet(
            "The Nobel Peace Prize was announced today"
        )

        self.assertTrue(segments)
        self.assertTrue(
            any("nobel" in segment and "peace" in segment for segment in segments)
        )

    def test_preserves_hashtags(self):
        segments = segment_tweet(
            "Everyone is discussing #NobelPrize today"
        )

        self.assertTrue(
            any("#nobelprize" in segment.lower() for segment in segments)
        )

    def test_empty_text_returns_no_segments(self):
        self.assertEqual(segment_tweet(""), [])

    def test_repeated_input_is_deterministic(self):
        text = "Boston Marathon bombing news"

        self.assertEqual(segment_tweet(text), segment_tweet(text))


if __name__ == "__main__":
    unittest.main()
