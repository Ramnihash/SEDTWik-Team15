
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


GENERIC_TERMS = {
    "rt", "read", "amp", "year", "old", "today", "breaking",
    "news", "people", "time", "go", "goes", "get", "got",
    "one", "two", "via", "http", "https", "com", "r", "p",
    "died", "running", "girl"
}


def clean_segment(segment):
    words = re.findall(r"[a-z]+", segment.lower())
    words = [word for word in words if word not in GENERIC_TERMS]

    if len(words) < 2:
        return ""

    return " ".join(words)


def cluster_segments(segments, threshold=0.45):
    cleaned_to_original = {}

    for segment in segments:
        if not segment:
            continue

        cleaned = clean_segment(segment)

        if cleaned:
            cleaned_to_original.setdefault(cleaned, segment.strip().lower())

    cleaned_segments = list(cleaned_to_original.keys())

    if not cleaned_segments:
        return []

    if len(cleaned_segments) == 1:
        return [[cleaned_to_original[cleaned_segments[0]]]]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(cleaned_segments)
    similarity = cosine_similarity(matrix)

    ordered = sorted(
        range(len(cleaned_segments)),
        key=lambda i: (
            len(cleaned_segments[i].split()),
            similarity[i].sum()
        ),
        reverse=True
    )

    clusters = []
    used = set()

    for i in ordered:
        if i in used:
            continue

        cluster_indices = [i]
        used.add(i)

        for j in ordered:
            if j in used:
                continue

            if similarity[i][j] >= threshold:
                cluster_indices.append(j)
                used.add(j)

        cluster = [
            cleaned_to_original[cleaned_segments[index]]
            for index in cluster_indices
        ]

        clusters.append(cluster)

    return clusters


if __name__ == "__main__":
    sample_segments = [
        "boston marathon bombing",
        "marathon bombing suspect",
        "boston bombing",
        "sandy hook kids",
        "nobel peace prize",
        "peace prize",
        "justin bieber"
    ]

    clusters = cluster_segments(sample_segments)

    for i, cluster in enumerate(clusters, 1):
        print(f"Cluster {i}:", cluster)
