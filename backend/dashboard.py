import streamlit as st

from dashboard.components.trending_event import show_trending_events
from dashboard.components.data_loader import load_data
from dashboard.components.search import search_events
from dashboard.components.event_view import show_event
from dashboard.components.statistics import show_statistics

# -----------------------
# Page Config
# -----------------------

st.set_page_config(
    page_title="AI News Intelligence Platform",
    page_icon="📰",
    layout="wide"
)

# -----------------------
# Header
# -----------------------

st.title("📰 AI News Intelligence Platform")

st.markdown("""
Detect, cluster and analyze real-time news events using

- Sentence Transformers
- Agglomerative Clustering
- Named Entity Recognition
- Keyword Extraction
""")

st.divider()

# -----------------------
# Load Data
# -----------------------

df, titles_df = load_data()

# -----------------------
# Dashboard Overview
# -----------------------

show_trending_events(df, titles_df)

st.divider()
st.subheader("📊 Dashboard Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Articles", len(df))

with c2:
    st.metric("Sources", df["source"].nunique())

with c3:
    st.metric("Events", df["cluster"].nunique())

st.divider()

# -----------------------
# Search
# -----------------------

df = search_events(df)


# -----------------------
# Event
# -----------------------
clusters = sorted(df["cluster"].unique())

if "selected_cluster" not in st.session_state:
    st.session_state.selected_cluster = clusters[0]

if st.session_state.selected_cluster not in clusters:
    st.session_state.selected_cluster = clusters[0]
    
cluster_df = df[
    df["cluster"] == st.session_state.selected_cluster
]

show_event(
    cluster_df,
    st.session_state.selected_cluster,
    titles_df
)   

# -----------------------
# Statistics
# -----------------------

show_statistics(cluster_df)