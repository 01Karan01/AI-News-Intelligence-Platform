import streamlit as st


def sidebar(df):

    st.sidebar.title("📰 AI News")
    st.sidebar.markdown("---")

    clusters = sorted(df["cluster"].unique())

    # Initialize session state
    if "selected_cluster" not in st.session_state:
        st.session_state.selected_cluster = clusters[0]

    # If current cluster disappeared after search
    if st.session_state.selected_cluster not in clusters:
        st.session_state.selected_cluster = clusters[0]

    selected_cluster = st.sidebar.selectbox(
        "📌 Select Event",
        options=clusters,
        key="selected_cluster"
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("📊 Event Summary")

    for cluster in clusters:
        count = len(df[df["cluster"] == cluster])
        st.sidebar.caption(f"Event {cluster} • {count} Articles")

    return selected_cluster