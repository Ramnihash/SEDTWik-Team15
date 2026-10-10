
from collections import defaultdict
from datetime import datetime, timedelta


def classify_event_activity(previous_count, current_count):
    if previous_count < 0 or current_count < 0:
        raise ValueError("Activity counts cannot be negative")

    if previous_count == 0 and current_count > 0:
        return "Emerging"

    if previous_count == 0 and current_count == 0:
        return "Inactive"

    change_ratio = (current_count - previous_count) / previous_count

    if change_ratio >= 0.5:
        return "Growing"

    if change_ratio <= -0.5:
        return "Declining"

    return "Stable"


def analyze_event_novelty(tweets, event_segments, window_hours=24, now=None):
    if window_hours <= 0:
        raise ValueError("Window size must be positive")

    if now is None:
        now = datetime.now()

    previous_start = now - timedelta(hours=2 * window_hours)
    current_start = now - timedelta(hours=window_hours)

    counts = defaultdict(int)

    for tweet in tweets:
        timestamp = tweet.get("timestamp")
        text = str(tweet.get("text", "")).lower()

        if not timestamp or str(timestamp).lower() in {
            "historical_unknown", "unknown", "none", "nan"
        }:
            continue

        try:
            tweet_time = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        except ValueError:
            continue

        reference_now = now
        if tweet_time.tzinfo is not None and reference_now.tzinfo is None:
            reference_now = reference_now.replace(tzinfo=tweet_time.tzinfo)
        elif tweet_time.tzinfo is None and reference_now.tzinfo is not None:
            tweet_time = tweet_time.replace(tzinfo=reference_now.tzinfo)

        if tweet_time < previous_start or tweet_time > reference_now:
            continue

        for event, segments in event_segments.items():
            if any(segment.lower() in text for segment in segments):
                if tweet_time < current_start:
                    counts[(event, "previous")] += 1
                else:
                    counts[(event, "current")] += 1

    results = {}

    for event in event_segments:
        previous_count = counts[(event, "previous")]
        current_count = counts[(event, "current")]

        results[event] = {
            "previous_count": previous_count,
            "current_count": current_count,
            "status": classify_event_activity(previous_count, current_count)
        }

    return results
