import streamlit as st
from dashboard.components.icons import get_event_icon


def show_trending_events(df, titles_df):

    st.subheader("🔥 Top AI-Detected Events")

    # Count articles in each cluster
    cluster_sizes = (
        df.groupby("cluster")
        .size()
        .sort_values(ascending=False)
    )

    top_clusters = cluster_sizes.head(6)

    clusters = list(top_clusters.items())

    # Display cards in rows of 3
    for row in range(0, len(clusters), 3):

        cols = st.columns(3)

        for col, (cluster, count) in zip(cols, clusters[row:row + 3]):

            with col:

                title_row = titles_df[
                    titles_df["cluster"] == cluster
                ]

                if not title_row.empty:
                    event_name = title_row.iloc[0]["keywords"].title()
                else:
                    event_name = f"Event {cluster}"

                icon = get_event_icon(event_name)

                sources = (
                    df[df["cluster"] == cluster]["source"]
                    .unique()
                )

                with st.container(border=True):

                    st.markdown(f"## {icon} {event_name}")

                    st.write(f"**📰 Articles:** {count}")

                    st.write(
                        f"**📡 Sources:** {', '.join(sources[:2])}"
                    )

                    st.progress(min(count / 20, 1.0))

                    if st.button(
                    f"📖 Open Event",
                    key=f"cluster_{cluster}",
                    use_container_width=True
                    ):
                        st.session_state.selected_cluster = cluster
                        st.rerun()