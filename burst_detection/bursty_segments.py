def find_bursty_segments(segment_index, min_frequency=2, min_score=1.0):
    bursty = {}

    for segment, tweets in segment_index.items():
        frequency = len(tweets)

        if frequency < min_frequency:
            continue

        timestamps = [
            tweet["timestamp"]
            for tweet in tweets
        ]

        unique_dates = len(set(timestamps))

        if unique_dates == 0:
            continue

        score = frequency / unique_dates

        if score >= min_score:
            bursty[segment] = {
                "frequency": frequency,
                "timestamps": timestamps,
                "score": score
            }

    return bursty


if __name__ == "__main__":
    sample_index = {
        "nobel peace prize": [
            {"tweet_id": 1, "timestamp": "2026-10-01"},
            {"tweet_id": 2, "timestamp": "2026-10-01"},
            {"tweet_id": 3, "timestamp": "2026-10-02"}
        ],
        "breaking news": [
            {"tweet_id": 1, "timestamp": "2026-10-01"}
        ]
    }

    bursty = find_bursty_segments(sample_index)

    print("Bursty Segments:")

    for segment, data in bursty.items():
        print(segment, "->", data)