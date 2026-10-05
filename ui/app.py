import sys
from pathlib import Path

import streamlit as st
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from segmentation.segmenter import segment_tweet
from indexing.segment_index import build_segment_index
from burst_detection.bursty_segments import find_bursty_segments
from clustering.event_cluster import cluster_segments
from summarization.event_summary import summarize_event
from segmentation.wikipedia_filter import filter_wikipedia_segments


st.set_page_config(
    page_title="SEDTWik Event Detection",
    page_icon="📡",
    layout="wide"
)

st.title("SEDTWik: Event Detection from Tweets")
st.write("Segmentation-based event detection using bursty segments and TF-IDF clustering")

st.divider()

st.subheader("Tweet Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV file containing tweets",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    tweet_segments = []

    for _, row in df.iterrows():
        segments = segment_tweet(row["text"])

        tweet_segments.append(
            (
                row["tweet_id"],
                row["timestamp"],
                segments
            )
        )

    segment_index = build_segment_index(tweet_segments)

    bursty = find_bursty_segments(
        segment_index,
        min_frequency=2
    )

    segments = [
        segment
        for segment in bursty.keys()
        if not segment.startswith("#")
    ]

    wikipedia_segments = filter_wikipedia_segments(segments)

    if wikipedia_segments:
        segments = wikipedia_segments

    clusters = cluster_segments(segments)

    events = []

    for cluster in clusters:
        summary = summarize_event(cluster)

        frequency = max(
            bursty[segment]["frequency"] * bursty[segment]["hashtag_weight"]
            for segment in cluster
        )

        score = max(
            bursty[segment]["score"]
            for segment in cluster
        )

        events.append({
            "summary": summary,
            "frequency": frequency,
            "score": score,
            "segments": cluster
        })

    st.success("Dataset uploaded and processed successfully.")

    st.divider()

    st.subheader("Dataset Statistics")

    col1, col2, col3, col4 = st.columns(4)

    total_tweets = len(df)
    total_events = len(events)

    if total_events > 0:
        average_frequency = sum(
            event["frequency"]
            for event in events
        ) / total_events

        average_score = sum(
            event["score"]
            for event in events
        ) / total_events
    else:
        average_frequency = 0
        average_score = 0

    col1.metric("Total Tweets", total_tweets)
    col2.metric("Detected Events", total_events)
    col3.metric("Average Frequency", round(average_frequency, 2))
    col4.metric("Average Burst Score", round(average_score, 2))

    st.divider()

    st.subheader("Detected Events")

    if not events:
        st.warning("No events detected.")
    else:
        for i, event in enumerate(events, 1):
            with st.container():
                st.markdown(f"### Event {i}")
                st.write("**Event:**", event["summary"])

                col1, col2 = st.columns(2)

                col1.metric(
                    "Frequency",
                    event["frequency"]
                )

                col2.metric(
                    "Burst Score",
                    round(event["score"], 2)
                )

                st.write(
                    "**Related Segments:**",
                    ", ".join(event["segments"])
                )

                st.divider()