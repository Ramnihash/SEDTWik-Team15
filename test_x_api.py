
import os
import requests
from dotenv import load_dotenv

load_dotenv()

bearer_token = os.getenv("X_BEARER_TOKEN")

if not bearer_token:
    print("ERROR: X_BEARER_TOKEN was not found in .env")
    raise SystemExit(1)

url = "https://api.x.com/2/tweets/search/recent"

headers = {
    "Authorization": f"Bearer {bearer_token}"
}

params = {
    "query": '"Nobel Peace Prize" -is:retweet',
    "max_results": 10,
    "tweet.fields": "created_at,public_metrics"
}

try:
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    print("HTTP Status:", response.status_code)

    if response.ok:
        result = response.json()
        tweets = result.get("data", [])
        print("Tweets retrieved:", len(tweets))

        for tweet in tweets:
            print("-", tweet.get("created_at", "Unknown date"))
            print(tweet.get("text", ""))
            print()
    else:
        print("API response:")
        print(response.text[:2000])

except requests.RequestException as error:
    print("Connection error:", error)
