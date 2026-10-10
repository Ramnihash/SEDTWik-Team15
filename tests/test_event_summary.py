
import unittest

from summarization.event_summary import summarize_event


class TestEventSummary(unittest.TestCase):
    def test_generates_summary_for_related_segments(self):
        segments = [
            "boston marathon bombing",
            "boston marathon explosion",
            "marathon bombing suspect"
        ]

        summary = summarize_event(segments)

        self.assertIsInstance(summary, str)
        self.assertTrue(summary.strip())

    def test_summary_is_deterministic(self):
        segments = [
            "nobel peace prize",
            "nobel peace prize winner"
        ]

        first = summarize_event(segments)
        second = summarize_event(segments)

        self.assertEqual(first, second)

    def test_empty_segments(self):
        summary = summarize_event([])

        self.assertIsInstance(summary, str)

    def test_single_segment(self):
        summary = summarize_event(["nobel peace prize"])

        self.assertIsInstance(summary, str)
        self.assertTrue(summary.strip())


if __name__ == "__main__":
    unittest.main()
