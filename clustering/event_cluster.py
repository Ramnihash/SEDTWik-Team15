import itertools
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


GENERIC_TERMS = {
    "rt", "read", "amp", "year", "old", "today", "breaking",
    "news", "people", "time", "go", "goes", "get", "got",
    "one", "two", "via", "http", "https", "com", "died",
    "running", "girl", "latest", "update"
}


def clean_segment(segment):
    words = re.findall(r"[a-z]+", segment.lower())
    words = [word for word in words if word not in GENERIC_TERMS]

    if len(words) < 2 or len("".join(words)) < 6:
        return ""

    return " ".join(words)


def token_overlap(first, second):
    first_words = set(first.split())
    second_words = set(second.split())

    if not first_words or not second_words:
        return 0.0

    return len(first_words & second_words) / len(first_words | second_words)


def is_conflicting_event(first, second):
    first_words = set(first.split())
    second_words = set(second.split())

    explosion_terms = {"bombing", "bomb", "explosion", "explosions"}
    finish_terms = {"finish", "line"}

    first_is_explosion = bool(first_words & explosion_terms)
    second_is_explosion = bool(second_words & explosion_terms)
    first_is_finish = bool(first_words & finish_terms)
    second_is_finish = bool(second_words & finish_terms)

    return (
        (first_is_explosion and second_is_finish)
        or (second_is_explosion and first_is_finish)
    )


def cluster_segments(segments, threshold=0.4):
    cleaned_to_originals = {}

    for segment in segments:
        if not segment:
            continue

        original = segment.strip().lower()
        cleaned = clean_segment(original)

        if cleaned:
            originals = cleaned_to_originals.setdefault(cleaned, [])

            if original not in originals:
                originals.append(original)

    cleaned_segments = sorted(cleaned_to_originals)

    if not cleaned_segments:
        return []

    if len(cleaned_segments) == 1:
        return [cleaned_to_originals[cleaned_segments[0]]]

    matrix = TfidfVectorizer(
        ngram_range=(1, 2)
    ).fit_transform(cleaned_segments)

    similarities = cosine_similarity(matrix)
    words = [set(cleaned.split()) for cleaned in cleaned_segments]

    # Build candidate links between segments
    edges = []

    for i, j in itertools.combinations(range(len(cleaned_segments)), 2):
        if len(words[i] & words[j]) < 2:
            continue

        if words[i] <= words[j] or words[j] <= words[i]:
            score = 1.0
        elif (
            similarities[i][j] >= threshold
            and token_overlap(cleaned_segments[i], cleaned_segments[j]) >= 0.4
        ):
            score = similarities[i][j]
        else:
            continue

        edges.append((score, i, j))

    edges.sort(key=lambda edge: -edge[0])  # strongest links first

    # Merge clusters, but never join two clusters that contain a conflicting pair
    members = {i: [i] for i in range(len(cleaned_segments))}
    root = list(range(len(cleaned_segments)))

    for _, i, j in edges:
        a, b = root[i], root[j]

        if a == b:
            continue

        if any(
            is_conflicting_event(cleaned_segments[x], cleaned_segments[y])
            for x in members[a]
            for y in members[b]
        ):
            continue

        for x in members[b]:
            root[x] = a

        members[a] += members.pop(b)

    return [
        [
            original
            for i in group
            for original in cleaned_to_originals[cleaned_segments[i]]
        ]
        for group in members.values()
    ]


if __name__ == "__main__":
    sample_segments = [
        "boston marathon",
        "marathon explosion",
        "boston marathon explosion",
        "boston marathon finish",
        "marathon finish",
        "finish line",
        "marathon finish line",
        "nobel peace prize",
        "peace prize",
    ]

    for index, cluster in enumerate(cluster_segments(sample_segments), 1):
        print(f"Cluster {index}:", cluster)
    