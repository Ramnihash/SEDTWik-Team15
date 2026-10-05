import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def summarize_event(cluster):
    if not cluster:
        return ""

    if len(cluster) == 1:
        return cluster[0]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(cluster)

    similarity = cosine_similarity(matrix)

    graph = nx.from_numpy_array(similarity)

    scores = nx.pagerank(graph)

    best_index = max(scores, key=scores.get)

    return cluster[best_index]


if __name__ == "__main__":
    cluster = [
        "nobel peace prize",
        "nobel peace prize announced today",
        "peace prize ceremony today"
    ]

    print("Event Summary:")
    print(summarize_event(cluster))