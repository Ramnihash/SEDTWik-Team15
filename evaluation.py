def evaluate_events(tweets, events):
    total_tweets = len(tweets)
    total_events = len(events)

    if total_events == 0:
        return {
            "total_tweets": total_tweets,
            "total_events": 0,
            "average_frequency": 0,
            "average_burst_score": 0
        }

    frequencies = [event["frequency"] for event in events]
    burst_scores = [event["burst_score"] for event in events]

    return {
        "total_tweets": total_tweets,
        "total_events": total_events,
        "average_frequency": sum(frequencies) / total_events,
        "average_burst_score": sum(burst_scores) / total_events
    }


if __name__ == "__main__":
    tweets = [1, 2, 3, 4, 5, 6, 7, 8]

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
    print("Average Frequency:", result["average_frequency"])
    print("Average Burst Score:", result["average_burst_score"])