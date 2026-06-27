import streamlit as st
import pandas as pd

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="AI News Intelligence",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI News Intelligence Platform")

st.write("### Clustered News Events")

# ----------------------------
# Load Data
# ----------------------------

df = pd.read_csv("clustered_news.csv")

clusters = sorted(df["cluster"].unique())

# ----------------------------
# Display Each Cluster
# ----------------------------

for cluster in clusters:

    cluster_df = df[df["cluster"] == cluster]

    with st.expander(f"📌 Event Cluster {cluster}"):

        st.write(f"**Articles:** {len(cluster_df)}")

        st.write("### Headlines")

        for title in cluster_df["title"]:
            st.write("- " + title)