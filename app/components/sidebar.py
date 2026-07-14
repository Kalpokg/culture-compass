import streamlit as st


def sidebar(df):

    st.sidebar.header("🔍 Search")

    query = st.sidebar.text_input(
        "Keyword"
    )

    cities = ["All"] + sorted(
        df["city"].dropna().unique().tolist()
    )

    city = st.sidebar.selectbox(
        "City",
        cities,
    )

    if city == "All":
        city = None

    return query, city