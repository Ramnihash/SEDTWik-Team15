from collections import defaultdict


def build_segment_index(tweets):
    index = defaultdict(list)

    for tweet_id, timestamp, segments in tweets:
        for segment in segments:
            index[segment].append({
                "tweet_id": tweet_id,
                "timestamp": timestamp
            })

    return dict(index)


if __name__ == "__main__":
    sample_data = [
        (
            1,
            "2026-10-01",
            ["breaking news", "nobel peace prize"]
        ),
        (
            2,
            "2026-10-01",
            ["nobel peace prize", "ceremony happening"]
        ),
    ]

    index = build_segment_index(sample_data)

    print("Segment Index:")

    for segment, tweets in index.items():
        print(segment, "->", tweets)
    