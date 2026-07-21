import streamlit as st

from culture_compass.services.event_service import EventService


def sidebar(service: EventService):

    st.sidebar.header("🔍 Search")

    # Keyword
    query = st.sidebar.text_input("Keyword")

    # Country
    countries = ["All"] + service.get_countries()

    country = st.sidebar.selectbox(
        "Country",
        countries,
    )

    if country == "All":
        country = None

    # City
    cities = ["All"] + service.get_cities(country)

    city = st.sidebar.selectbox(
        "City",
        cities,
    )

    if city == "All":
        city = None

    # Genre
    genres = ["All"] + service.get_genres()

    genre = st.sidebar.selectbox(
        "Genre",
        genres,
    )

    if genre == "All":
        genre = None

    # Date range
    st.sidebar.subheader("📅 Date Range")

    start_date = st.sidebar.date_input(
        "From",
        value=None,
    )

    end_date = st.sidebar.date_input(
        "To",
        value=None,
    )

    return (
        query,
        country,
        city,
        genre,
        start_date,
        end_date,
    )