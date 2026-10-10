import re


WIKIPEDIA_TERMS = {
    "nobel peace prize",
    "justin bieber",
    "presidential debate",
    "national coming out day"
}


def normalize_phrase(segment):
    return re.sub(r"\s+", " ", segment.lower()).strip()


def is_wikipedia_phrase(segment):
    normalized = normalize_phrase(segment)
    return any(
        term == normalized or term in normalized
        for term in WIKIPEDIA_TERMS
    )


def filter_wikipedia_segments(segments):
    return [
        segment
        for segment in segments
        if is_wikipedia_phrase(segment)
    ]


if __name__ == "__main__":
    segments = [
        "nobel peace prize",
        "random phrase",
        "justin bieber",
        "presidential debate",
        "national coming out day celebration"
    ]

    print(filter_wikipedia_segments(segments))
    