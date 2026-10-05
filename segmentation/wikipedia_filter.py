import re


WIKIPEDIA_TERMS = {
    "nobel peace prize",
    "justin bieber",
    "presidential debate",
    "national coming out day"
}


def is_wikipedia_phrase(segment):
    normalized = re.sub(r"\s+", " ", segment.lower()).strip()
    return normalized in WIKIPEDIA_TERMS


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
        "presidential debate"
    ]

    print(filter_wikipedia_segments(segments))
    