from collections import Counter


def summarize_event(cluster):
    if not cluster:
        return ""

    counts = Counter(cluster)

    summary = max(
        cluster,
        key=lambda segment: (
            len(segment.split()),
            counts[segment]
        )
    )

    return summary


if __name__ == "__main__":
    sample_cluster = [
        "nobel peace prize",
        "nobel peace prize announced today",
        "peace prize ceremony",
        "nobel peace prize"
    ]

    summary = summarize_event(sample_cluster)

    print("Event Summary:")
    print(summary)