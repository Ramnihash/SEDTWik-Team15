import re


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^\w\s#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text):
    return clean_text(text).split()


def extract_hashtags(text):
    return re.findall(r"#\w+", str(text).lower())


if __name__ == "__main__":
    sample = "Breaking News! #NobelPrize announced today @news"

    print("Original:", sample)
    print("Cleaned:", clean_text(sample))
    print("Tokens:", tokenize(sample))
    print("Hashtags:", extract_hashtags(sample))