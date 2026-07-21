import streamlit as st

from culture_compass.dto.event import EventDTO


def event_card(event: EventDTO) -> bool:
    """
    Display an event search result card.
    """

    with st.container(border=True):

        # -------------------------------------------------
        # Event Image
        # -------------------------------------------------

        if event.image_url:
            st.image(event.image_url, width="stretch")

        # -------------------------------------------------
        # Event Title
        # -------------------------------------------------

        st.markdown(
            f"### {event.event_name}"
        )

        # -------------------------------------------------
        # Event Metadata
        # -------------------------------------------------

        st.caption(
            f"📍 {event.city.title()} • "
            f"📅 {event.event_date.strftime('%d %b %Y')}"
        )

        st.markdown(
            f"**🎵 {event.genre.title()}**"
        )

        st.write("")

        # -------------------------------------------------
        # Select Button
        # -------------------------------------------------

        return st.button(
            "Select",
            key=event.id,
            width="stretch",
        )