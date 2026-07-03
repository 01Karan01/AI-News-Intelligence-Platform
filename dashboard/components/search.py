import streamlit as st


def search_events(df):

    search_query = st.text_input(
        "🔍 Search Events",
        placeholder="OpenAI, Iran, GTA 6, Heatwave..."
    )

    if search_query:

        matching_clusters = df[
            df["title"].str.contains(search_query, case=False, na=False) |
            df["summary"].str.contains(search_query, case=False, na=False)
        ]["cluster"].unique()

        df = df[df["cluster"].isin(matching_clusters)]

    if df.empty:
        st.warning("⚠️ No matching events found.")
        st.stop()

    return df