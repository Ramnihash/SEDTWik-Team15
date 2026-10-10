
import unittest

from clustering.event_cluster import cluster_segments


class TestEventClustering(unittest.TestCase):
    def test_related_boston_phrases_are_clustered(self):
        segments = [
            "boston marathon bombing",
            "marathon bombing suspect",
            "boston bombing",
            "boston marathon explosion"
        ]

        clusters = cluster_segments(segments)

        self.assertTrue(
            any(
                len(set(segments).intersection(cluster)) == len(segments)
                for cluster in clusters
            )
        )

    def test_unrelated_events_remain_separate(self):
        segments = [
            "boston marathon bombing",
            "sandy hook kids",
            "nobel peace prize",
            "justin bieber"
        ]

        clusters = cluster_segments(segments)

        for first, second in [
            ("boston marathon bombing", "sandy hook kids"),
            ("boston marathon bombing", "nobel peace prize"),
            ("sandy hook kids", "justin bieber"),
            ("nobel peace prize", "justin bieber")
        ]:
            self.assertFalse(
                any(first in cluster and second in cluster for cluster in clusters),
                f"Unrelated phrases were merged: {first} and {second}"
            )

    def test_nobel_variants_are_clustered(self):
        segments = ["nobel peace prize", "peace prize"]

        clusters = cluster_segments(segments)

        self.assertTrue(
            any(all(segment in cluster for segment in segments) for cluster in clusters)
        )

    def test_empty_input_returns_no_clusters(self):
        self.assertEqual(cluster_segments([]), [])

    def test_duplicate_phrases_do_not_create_duplicate_entries(self):
        clusters = cluster_segments([
            "nobel peace prize",
            "nobel peace prize"
        ])

        self.assertEqual(len(clusters), 1)
        self.assertEqual(clusters[0], ["nobel peace prize"])
    
    def test_unrelated_finish_line_phrases_stay_separate(self):
        segments = [
            "boston marathon",
            "marathon explosion",
            "boston marathon explosion",
            "marathon finish",
            "finish line",
            "marathon finish line"
        ]

        clusters = cluster_segments(segments)

        explosion_cluster = next(
            cluster
            for cluster in clusters
            if "boston marathon explosion" in cluster
        )

        self.assertNotIn("finish line", explosion_cluster)
        self.assertNotIn("marathon finish line", explosion_cluster)


if __name__ == "__main__":
    unittest.main()
