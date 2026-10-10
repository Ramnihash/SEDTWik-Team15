
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

        valid_timestamps = [
            timestamp
            for timestamp in timestamps
            if timestamp
            and str(timestamp).lower() not in {"historical_unknown", "unknown", "none", "nan"}
        ]

        if not valid_timestamps:
            continue

        unique_dates = len(set(valid_timestamps))

        hashtag_weight = 2 if tweets[0]["is_hashtag"] else 1
        score = (frequency / unique_dates) * hashtag_weight

        if score >= min_score:
            bursty[segment] = {
                "frequency": frequency,
                "timestamps": valid_timestamps,
                "score": score,
                "hashtag_weight": hashtag_weight
            }

    return bursty


if __name__ == "__main__":
    segment_index = {
        "nobel peace prize": [
            {
                "tweet_id": 1,
                "timestamp": "2026-10-01",
                "is_hashtag": False
            },
            {
                "tweet_id": 2,
                "timestamp": "2026-10-01",
                "is_hashtag": False
            }
        ],
        "#nobelprize": [
            {
                "tweet_id": 1,
                "timestamp": "2026-10-01",
                "is_hashtag": True
            },
            {
                "tweet_id": 2,
                "timestamp": "2026-10-01",
                "is_hashtag": True
            }
        ]
    }

    result = find_bursty_segments(segment_index)

    print(result)
