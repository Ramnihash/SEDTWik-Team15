
import unittest
from datetime import datetime, timezone

from novelty.novelty_detector import (
    classify_event_activity,
    analyze_event_novelty
)


class TestNoveltyDetector(unittest.TestCase):
    def test_new_event_is_emerging(self):
        self.assertEqual(
            classify_event_activity(0, 5),
            "Emerging"
        )

    def test_activity_increase_is_growing(self):
        self.assertEqual(
            classify_event_activity(10, 16),
            "Growing"
        )

    def test_similar_activity_is_stable(self):
        self.assertEqual(
            classify_event_activity(10, 12),
            "Stable"
        )

    def test_activity_decrease_is_declining(self):
        self.assertEqual(
            classify_event_activity(10, 4),
            "Declining"
        )

    def test_zero_activity_is_inactive(self):
        self.assertEqual(
            classify_event_activity(0, 0),
            "Inactive"
        )

    def test_negative_counts_are_rejected(self):
        with self.assertRaises(ValueError):
            classify_event_activity(-1, 2)

    def test_unknown_timestamps_are_ignored(self):
        now = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)
        tweets = [
            {
                "timestamp": "historical_unknown",
                "text": "boston marathon bombing"
            }
        ]

        result = analyze_event_novelty(
            tweets,
            {"Boston event": ["boston marathon bombing"]},
            window_hours=24,
            now=now
        )

        self.assertEqual(result["Boston event"]["previous_count"], 0)
        self.assertEqual(result["Boston event"]["current_count"], 0)
        self.assertEqual(result["Boston event"]["status"], "Inactive")

    def test_recent_tweets_are_counted(self):
        now = datetime(2026, 10, 10, 12, 0, tzinfo=timezone.utc)
        tweets = [
            {
                "timestamp": "2026-10-10T10:00:00+00:00",
                "text": "boston marathon bombing update"
            },
            {
                "timestamp": "2026-10-10T11:00:00+00:00",
                "text": "another boston marathon bombing report"
            }
        ]

        result = analyze_event_novelty(
            tweets,
            {"Boston event": ["boston marathon bombing"]},
            window_hours=24,
            now=now
        )

        self.assertEqual(result["Boston event"]["current_count"], 2)
        self.assertEqual(result["Boston event"]["status"], "Emerging")


if __name__ == "__main__":
    unittest.main()
