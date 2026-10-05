import re


def segment_tweet(text):
    text = str(text).lower()
    hashtags = re.findall(r"#\w+", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    words = text.split()

    segments = []

    for n in range(2, 6):
        for i in range(len(words) - n + 1):
            segment = " ".join(words[i:i + n])
            segments.append(segment)

    segments.extend(hashtags)

    return segments


if __name__ == "__main__":
    tweet = "Breaking news: Nobel Peace Prize announced today #NobelPrize"

    print("Tweet:", tweet)
    print("Segments:", segment_tweet(tweet))