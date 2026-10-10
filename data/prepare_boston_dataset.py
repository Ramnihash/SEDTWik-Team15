
import pandas as pd

source_path = "data/2013_Boston_bombings-tweets_labeled.csv"
output_path = "data/boston_tweets.csv"

df = pd.read_csv(source_path)
df.columns = df.columns.str.strip()

df = df.dropna(subset=["Tweet ID", "Tweet Text"]).copy()
df = df.drop_duplicates(subset=["Tweet ID"])

df["tweet_id"] = df["Tweet ID"].astype(str)
df["text"] = df["Tweet Text"].astype(str)
df["timestamp"] = "historical_unknown"

df[[
    "tweet_id",
    "timestamp",
    "text",
    "Informativeness"
]].to_csv(output_path, index=False)

print("Prepared tweets:", len(df))
print("Saved to:", output_path)
print("Columns:", ["tweet_id", "timestamp", "text", "Informativeness"])
