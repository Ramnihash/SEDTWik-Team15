import re
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))
STOP_WORDS.discard("out")


def segment_tweet(text):
    text = str(text).lower()
    hashtags = re.findall(r"#\w+", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"#\w+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)

    words = [
        word
        for word in text.split()
        if word not in STOP_WORDS and not word.isdigit()
    ]

    segments = []

    for n in range(2, 6):
        for i in range(len(words) - n + 1):
            segments.append(" ".join(words[i:i + n]))

    segments.extend(hashtags)

    return segments


if __name__ == "__main__":
    tweet = "National Coming Out Day celebrations today #ComingOutDay"
    print("Tweet:", tweet)
    print("Segments:", segment_tweet(tweet))
    