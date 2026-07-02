import streamlit as st


def get_event_name(selected_cluster, titles_df):

    match = titles_df[titles_df["cluster"] == selected_cluster]

    if match.empty:
        return f"Cluster {selected_cluster}"

    return match.iloc[0]["keywords"]


def show_event(cluster_df, selected_cluster, titles_df):

    event_name = get_event_name(selected_cluster, titles_df)

    # ----------------------------
    # Event Header
    # ----------------------------

    st.header(f"📰 {event_name.title()}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📰 Articles", len(cluster_df))

    with col2:
        st.metric("🌐 Sources", cluster_df["source"].nunique())

    st.divider()

    # ----------------------------
    # Headlines
    # ----------------------------

    st.subheader("📰 Latest Headlines")

    for _, row in cluster_df.iterrows():

        with st.container(border=True):

            st.markdown(f"### 📰 {row['title']}")

            st.caption(
                f"📍 {row['source']} | 🕒 {row['published']}"
            )

            if row["summary"]:
                st.write(row["summary"])

            st.link_button(
                "📖 Read Full Article",
                row["link"]
            )