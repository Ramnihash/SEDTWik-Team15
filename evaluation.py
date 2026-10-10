import math


def evaluate_events(tweets, events):
    total_tweets = len(tweets)
    total_events = len(events)

    if total_events == 0:
        return {
            "total_tweets": total_tweets,
            "total_events": 0,
            "average_frequency": 0,
            "average_burst_score": 0,
            "events_per_100_tweets": 0,
            "event_coverage": 0,
            "highest_frequency": 0,
            "highest_burst_score": 0
        }

    frequencies = [
        max(0, event.get("frequency", 0))
        for event in events
    ]

    burst_scores = [
        event.get("burst_score", 0)
        for event in events
    ]

    frequencies = [
        value if isinstance(value, (int, float)) and math.isfinite(value) else 0
        for value in frequencies
    ]

    burst_scores = [
        value if isinstance(value, (int, float)) and math.isfinite(value) else 0
        for value in burst_scores
    ]

    total_event_frequency = sum(frequencies)

    return {
        "total_tweets": total_tweets,
        "total_events": total_events,
        "average_frequency": total_event_frequency / total_events,
        "average_burst_score": sum(burst_scores) / total_events,
        "events_per_100_tweets": (
            total_events / total_tweets * 100
            if total_tweets > 0 else 0
        ),
        "event_coverage": (
            min(total_event_frequency / total_tweets, 1.0)
            if total_tweets > 0 else 0
        ),
        "highest_frequency": max(frequencies),
        "highest_burst_score": max(burst_scores)
    }


def count_event_tweets(valid_segments, segment_index):
    tweet_ids = set()

    for segment in valid_segments:
        for tweet in segment_index.get(segment, []):
            tweet_id = tweet.get("tweet_id")

            if tweet_id is not None:
                tweet_ids.add(tweet_id)

    return len(tweet_ids)


if __name__ == "__main__":
    tweets = list(range(8))

    events = [
        {"frequency": 2, "burst_score": 2.0},
        {"frequency": 2, "burst_score": 2.0},
        {"frequency": 2, "burst_score": 2.0},
        {"frequency": 2, "burst_score": 2.0}
    ]

    result = evaluate_events(tweets, events)

    print("Evaluation Results")
    print("==================")
    print("Total Tweets:", result["total_tweets"])
    print("Total Events:", result["total_events"])
    print("Average Frequency:", round(result["average_frequency"], 2))
    print("Average Burst Score:", round(result["average_burst_score"], 2))
    print("Events per 100 Tweets:", round(result["events_per_100_tweets"], 2))
    print("Event Coverage:", round(result["event_coverage"] * 100, 2), "%")
    print("Highest Event Frequency:", result["highest_frequency"])
    print("Highest Burst Score:", result["highest_burst_score"])
    