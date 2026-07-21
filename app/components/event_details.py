import streamlit as st


def event_details(event):
    """
    Display the selected event.
    """

    st.subheader("🎭 Event Details")

    # -------------------------------------------------
    # Hero Image
    # -------------------------------------------------

    image = event.get("image_url")

    if isinstance(image, str) and image.strip():
            st.image(image, width="stretch")

    # -------------------------------------------------
    # Event Title
    # -------------------------------------------------

    st.markdown(
        f"# {event['event_name']}"
    )

    # -------------------------------------------------
    # Event Information
    # -------------------------------------------------

    st.markdown(
        f"**🎵 Genre:** {event['genre'].title()}"
    )

    st.markdown(
        f"**📍 City:** {event['city'].title()}"
    )

    st.markdown(
        f"**📅 Date:** {event['date'].strftime('%d %b %Y')}"
    )

    st.write("")

    # -------------------------------------------------
    # Ticket Button
    # -------------------------------------------------

    st.link_button(
        "🎟 Buy Tickets",
        event["url"],
        width="stretch",
    )