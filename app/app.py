import streamlit as st
from pathlib import Path

from culture_compass.data.loader import load_dataset
from culture_compass.search.event_search import EventSearch
from culture_compass.recommender.content_based import (
    ContentBasedRecommender,
)

from app.components.sidebar import sidebar
from app.components.event_card import event_card
from app.components.event_details import event_details
from app.components.recommendations import recommendation_cards


def main():

    st.set_page_config(
        page_title="CultureCompass",
        page_icon="🎭",
        layout="wide",
    )

    css = Path("app/styles/style.css").read_text()

    st.markdown(
              f"<style>{css}</style>",
              unsafe_allow_html=True,
               )

    

    # =====================================================
    # Load Dataset
    # =====================================================

    df = load_dataset()

    # =====================================================
    # Header
    # =====================================================

    st.markdown("# 🎭 CultureCompass")

    st.markdown(
    """
       ### Discover concerts, theatre, museums and festivals across Europe.
    """
    )

    st.caption(
              f"{len(df):,} events • "
              f"{df['city'].nunique()} cities • "
              f"{df['country'].nunique()} countries"
    )

    st.divider()

    # =====================================================
    # Backend
    # =====================================================

    search = EventSearch(df)

    recommender = ContentBasedRecommender()
    recommender.fit(df)

    # =====================================================
    # Sidebar
    # =====================================================

    query, city = sidebar(df)

    # =====================================================
    # Search
    # =====================================================

    # =====================================================
    # Number of displayed results
    # =====================================================

    if "results_limit" not in st.session_state:
        st.session_state.results_limit = 20

    results = search.search(
           query=query if query else None,
           city=city,
           top_n=st.session_state.results_limit,
    )

    # =====================================================
    # Selected Event State
    # =====================================================

    if "selected_event" not in st.session_state:
        st.session_state.selected_event = None

    # =====================================================
    # Main Layout
    # =====================================================

    left, right = st.columns([1.1, 1.9], gap="large")

    # =====================================================
    # LEFT PANEL
    # =====================================================

    with left:

        st.subheader("🔍 Search Results")

        st.caption(
           f"Showing {len(results)} events"
        )

        if results.empty:

            st.info("No events found.")

        else:

            for _, event in results.iterrows():

                if event_card(event):

                   st.session_state.selected_event = event["event_id"]

                st.write("")

            if len(results) == st.session_state.results_limit:

               if st.button(
                    "Load More",
                     width="stretch",
                     ):

                  st.session_state.results_limit += 20

                  st.rerun()

    # =====================================================
    # RIGHT PANEL
    # =====================================================

    with right:

        if st.session_state.selected_event is None:

            st.info(
                "👈 Select an event from the left to view its details."
            )

        else:

            selected_event = df[
                df["event_id"]
                == st.session_state.selected_event
            ].iloc[0]

            # -------------------------
            # Event Details
            # -------------------------

            event_details(selected_event)

            # -------------------------
            # More Dates
            # -------------------------

            same_dates = recommender.recommend_same_event_dates(
                event_name=selected_event["event_name"],
                event_id=selected_event["event_id"],
                top_n=5,
            )

            recommendation_cards(
                "📅 More Dates",
                same_dates,
            )

            # -------------------------
            # Similar Events
            # -------------------------

            similar = recommender.recommend_similar_events(
                event_id=selected_event["event_id"],
                top_n=5,
            )

            recommendation_cards(
                "✨ Similar Events",
                similar,
            )


if __name__ == "__main__":
    main()