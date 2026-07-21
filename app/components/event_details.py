import streamlit as st

from culture_compass.dto.event import EventDTO


def event_details(event: EventDTO):
    """
    Display the selected event.
    """

    st.subheader("🎭 Event Details")

    # -------------------------------------------------
    # Hero Image
    # -------------------------------------------------

    if event.image_url:
        st.image(event.image_url, width="stretch")

    # -------------------------------------------------
    # Event Title
    # -------------------------------------------------

    st.markdown(
        f"# {event.event_name}"
    )

    # -------------------------------------------------
    # Event Information
    # -------------------------------------------------

    st.markdown(
        f"**🎵 Genre:** {event.genre.title()}"
    )

    st.markdown(
        f"**📍 Venue:** {event.venue}"
    )

    st.markdown(
        f"**🏙 City:** {event.city}"
    )

    st.markdown(
        f"**🌍 Country:** {event.country}"
    )

    st.markdown(
        f"**📅 Date:** {event.event_date.strftime('%d %b %Y')}"
    )

    if event.event_time:
        st.markdown(
            f"**🕒 Time:** {event.event_time.strftime('%H:%M')}"
        )

    st.write("")

    # -------------------------------------------------
    # Ticket Button
    # -------------------------------------------------

    if event.ticket_url:
        st.link_button(
            "🎟 Buy Tickets",
            event.ticket_url,
            width="stretch",
        )