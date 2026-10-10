
import unittest
from evaluation import count_event_tweets


class TestEventFrequency(unittest.TestCase):
    def test_duplicate_tweets_are_counted_once(self):
        segment_index = {
            "boston marathon": [
                {"tweet_id": "1"},
                {"tweet_id": "2"}
            ],
            "marathon bombing": [
                {"tweet_id": "2"},
                {"tweet_id": "3"}
            ]
        }

        result = count_event_tweets(
            ["boston marathon", "marathon bombing"],
            segment_index
        )

        self.assertEqual(result, 3)

    def test_missing_segments_do_not_add_tweets(self):
        self.assertEqual(
            count_event_tweets(
                ["unknown segment"],
                {}
            ),
            0
        )

    def test_empty_event_has_zero_frequency(self):
        self.assertEqual(
            count_event_tweets([], {}),
            0
        )


if __name__ == "__main__":
    unittest.main()
