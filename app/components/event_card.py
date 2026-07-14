import streamlit as st


def event_card(event):
    """
    Display an event as a search result card.
    """

    with st.container(border=True):

        # -------------------------------------------------
        # Event Image
        # -------------------------------------------------

        image = event.get("image_url")

        if image:
            st.image(
                image,
                width="stretch",
            )

        # -------------------------------------------------
        # Event Title
        # -------------------------------------------------

        st.markdown(
            f"### {event['event_name']}"
        )

        # -------------------------------------------------
        # Event Metadata
        # -------------------------------------------------

        st.caption(
            f"📍 {event['city'].title()} • "
            f"📅 {event['date'].strftime('%d %b %Y')}"
        )

        st.markdown(
            f"**🎵 {event['genre'].title()}**"
        )

        st.write("")

        # -------------------------------------------------
        # Select Button
        # -------------------------------------------------

        return st.button(
            "Select",
            key=event["event_id"],
            width="stretch",
        )