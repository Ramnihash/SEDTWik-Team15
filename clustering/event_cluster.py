from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cluster_segments(segments, threshold=0.25):
    if not segments:
        return []

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(segments)

    similarity = cosine_similarity(matrix)

    clusters = []
    used = set()

    ordered = sorted(
        range(len(segments)),
        key=lambda i: len(segments[i].split()),
        reverse=True
    )

    for i in ordered:
        if i in used:
            continue

        cluster = [segments[i]]
        used.add(i)

        for j in ordered:
            if j not in used and similarity[i][j] >= threshold:
                cluster.append(segments[j])
                used.add(j)

        clusters.append(cluster)

    return clusters


if __name__ == "__main__":
    sample_segments = [
        "nobel peace",
        "peace prize",
        "nobel peace prize",
        "justin bieber",
        "presidential debate",
        "national coming",
        "coming out",
        "national coming out",
        "coming out day",
        "national coming out day",
        "out day",
    ]

    clusters = cluster_segments(sample_segments)

    print("Event Clusters:")
    for i, cluster in enumerate(clusters, 1):
        print(f"Cluster {i}:", cluster)
    