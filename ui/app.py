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

    st.success("Dataset uploaded successfully.")

    st.write("Number of tweets:", len(df))

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

    clusters = cluster_segments(segments)

    st.divider()
    st.subheader("Detected Events")

    if not clusters:
        st.warning("No events detected.")
    else:
        for i, cluster in enumerate(clusters, 1):
            summary = summarize_event(cluster)

            frequency = max(
                bursty[segment]["frequency"] * bursty[segment]["hashtag_weight"]
                for segment in cluster
            )

            score = max(
                bursty[segment]["score"]
                for segment in cluster
            )

            with st.container():
                st.markdown(f"### Event {i}")
                st.write("**Event:**", summary)
                st.write("**Frequency:**", frequency)
                st.write("**Burst Score:**", round(score, 2))
                st.write("**Related Segments:**", ", ".join(cluster))
                st.divider()