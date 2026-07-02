import streamlit as st


def show_statistics(cluster_df):

    st.divider()

    st.subheader("📊 Event Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Articles",
            len(cluster_df)
        )

    with col2:
        st.metric(
            "Sources",
            cluster_df["source"].nunique()
        )

    with col3:
        st.metric(
            "Unique Titles",
            cluster_df["title"].nunique()
        )

    st.divider()

    st.subheader("📰 Articles by Source")

    source_counts = cluster_df["source"].value_counts()

    st.bar_chart(source_counts)

    st.divider()

    st.subheader("📋 Source Distribution")

    st.dataframe(
        source_counts.rename_axis("Source").reset_index(name="Articles"),
        use_container_width=True
    )