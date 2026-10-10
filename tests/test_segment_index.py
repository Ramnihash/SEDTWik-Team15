
import unittest

from indexing.segment_index import build_segment_index


class TestSegmentIndex(unittest.TestCase):
    def test_indexes_segments_from_tweets(self):
        tweets = [
            ("1", "2026-10-01", ["boston marathon", "#boston"]),
            ("2", "2026-10-02", ["boston marathon"])
        ]

        index = build_segment_index(tweets)

        self.assertIn("boston marathon", index)
        self.assertEqual(len(index["boston marathon"]), 2)

    def test_stores_tweet_ids_and_timestamps(self):
        tweets = [
            ("tweet-1", "2026-10-01", ["nobel peace prize"])
        ]

        index = build_segment_index(tweets)
        entry = index["nobel peace prize"][0]

        self.assertEqual(entry["tweet_id"], "tweet-1")
        self.assertEqual(entry["timestamp"], "2026-10-01")

    def test_identifies_hashtags(self):
        tweets = [
            ("1", "2026-10-01", ["#bostonmarathon"])
        ]

        index = build_segment_index(tweets)

        self.assertTrue(index["#bostonmarathon"][0]["is_hashtag"])

    def test_empty_input_returns_empty_index(self):
        self.assertEqual(build_segment_index([]), {})


if __name__ == "__main__":
    unittest.main()
