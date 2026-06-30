import streamlit as st
import pandas as pd

from utils.csv_utils import read_csv_safely

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI News Intelligence Platform",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI News Intelligence Platform")
st.markdown("### AI Powered News Event Detection")
st.write("---")

# ----------------------------
# Load Dataset
# ----------------------------
df = read_csv_safely("clustering/clustered_news.csv")
titles_df = pd.read_csv("data/event_titles.csv")
# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("Navigation")

clusters = sorted(df["cluster"].unique())

selected_cluster = st.sidebar.selectbox(
    "Select Event Cluster",
    clusters
)

# ----------------------------
# Display Event
# ----------------------------
cluster_df = df[df["cluster"] == selected_cluster]

event_name = titles_df[
    titles_df["cluster"] == selected_cluster
]["keywords"].values[0]

st.header(f"📰 {event_name.title()}")

st.metric("Articles", len(cluster_df))

st.write("---")

st.subheader("📰 Headlines")

for i, row in cluster_df.iterrows():
    st.markdown(f"### {row['title']}")
    st.write(f"**Source:** {row['source']}")
    st.write(f"**Published:** {row['published']}")
    st.markdown(f"[Read Full Article]({row['link']})")
    st.write("")

st.write("---")

# ----------------------------
# Statistics
# ----------------------------
st.subheader("📊 Event Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Articles", len(cluster_df))

with col2:
    st.metric("Sources", cluster_df["source"].nunique())

st.write("---")

# ----------------------------
# Source Distribution
# ----------------------------
st.subheader("📰 Articles by Source")

source_counts = cluster_df["source"].value_counts()

st.bar_chart(source_counts)

# ----------------------------
# All Events
# ----------------------------
st.sidebar.write("---")
st.sidebar.subheader("Available Events")

for c in clusters:
    st.sidebar.write(
        f"Cluster {c} ({len(df[df['cluster']==c])} articles)"
    )