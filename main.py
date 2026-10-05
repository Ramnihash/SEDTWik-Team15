import pandas as pd

from segmentation.segmenter import segment_tweet
from indexing.segment_index import build_segment_index
from burst_detection.bursty_segments import find_bursty_segments
from clustering.event_cluster import cluster_segments
from summarization.event_summary import summarize_event
from segmentation.wikipedia_filter import filter_wikipedia_segments


def main():
    df = pd.read_csv("data/tweets.csv")

    tweet_segments = []

    for _, row in df.iterrows():
        segments = segment_tweet(row["text"])

        tweet_segments.append(
            (
                row["tweet_id"],
                row["timestamp"],
                segments
            )
        )

    segment_index = build_segment_index(tweet_segments)

    bursty = find_bursty_segments(
        segment_index,
        min_frequency=2
    )

    segments = [
        segment
        for segment in bursty.keys()
        if not segment.startswith("#")
    ]

    wikipedia_segments = filter_wikipedia_segments(segments)

    if wikipedia_segments:
        segments = wikipedia_segments
    clusters = cluster_segments(segments)

    print("\nDetected Events")
    print("=" * 50)

    for i, cluster in enumerate(clusters, 1):
        summary = summarize_event(cluster)

        frequency = max(
            bursty[segment]["frequency"]
            for segment in cluster
        )

        score = max(
            bursty[segment]["score"]
            for segment in cluster
        )

        print(f"\nEvent {i}")
        print("Event:", summary)
        print("Frequency:", frequency)
        print("Burst Score:", round(score, 2))


if __name__ == "__main__":
    main()