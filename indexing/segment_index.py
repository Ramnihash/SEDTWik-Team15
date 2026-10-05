from collections import defaultdict


def build_segment_index(tweets):
    index = defaultdict(list)

    for tweet_id, timestamp, segments in tweets:
        for segment in segments:
            index[segment].append({
                "tweet_id": tweet_id,
                "timestamp": timestamp,
                "is_hashtag": segment.startswith("#")
            })

    return dict(index)


if __name__ == "__main__":
    tweets = [
        (
            1,
            "2026-10-01",
            ["nobel peace prize", "#nobelprize"]
        )
    ]

    index = build_segment_index(tweets)

    print(index)