
import unittest

from burst_detection.bursty_segments import find_bursty_segments


class TestBurstySegments(unittest.TestCase):
    def test_repeated_segment_is_detected(self):
        segment_index = {
            "boston marathon": [
                {"tweet_id": "1", "timestamp": "2026-10-01", "is_hashtag": False},
                {"tweet_id": "2", "timestamp": "2026-10-01", "is_hashtag": False}
            ]
        }

        result = find_bursty_segments(segment_index)

        self.assertIn("boston marathon", result)
        self.assertEqual(result["boston marathon"]["frequency"], 2)

    def test_hashtags_receive_double_weight(self):
        segment_index = {
            "#bostonmarathon": [
                {"tweet_id": "1", "timestamp": "2026-10-01", "is_hashtag": True},
                {"tweet_id": "2", "timestamp": "2026-10-01", "is_hashtag": True}
            ]
        }

        result = find_bursty_segments(segment_index)

        self.assertEqual(result["#bostonmarathon"]["hashtag_weight"], 2)
        self.assertEqual(result["#bostonmarathon"]["score"], 4)

    def test_unknown_timestamps_are_skipped(self):
        segment_index = {
            "historical event": [
                {"tweet_id": "1", "timestamp": "historical_unknown", "is_hashtag": False},
                {"tweet_id": "2", "timestamp": "historical_unknown", "is_hashtag": False}
            ]
        }

        result = find_bursty_segments(segment_index)

        self.assertNotIn("historical event", result)

    def test_segments_below_minimum_frequency_are_skipped(self):
        segment_index = {
            "rare phrase": [
                {"tweet_id": "1", "timestamp": "2026-10-01", "is_hashtag": False}
            ]
        }

        result = find_bursty_segments(segment_index, min_frequency=2)

        self.assertNotIn("rare phrase", result)

    def test_empty_index_returns_empty_result(self):
        self.assertEqual(find_bursty_segments({}), {})


if __name__ == "__main__":
    unittest.main()
