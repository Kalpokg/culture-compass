import streamlit as st


def recommendation_cards(title, df):
    """
    Display recommendation cards.
    """

    st.divider()
    st.subheader(title)

    if df.empty:
        st.info("No recommendations found.")
        return

    for _, row in df.iterrows():

        with st.container(border=True):

            # -------------------------------------------------
            # Event Image
            # -------------------------------------------------

            image = row.get("image_url")

            if isinstance(image, str) and image.strip():
               st.image(image, width="stretch")

            # -------------------------------------------------
            # Event Title
            # -------------------------------------------------

            st.markdown(
                f"### {row['event_name']}"
            )

            # -------------------------------------------------
            # Event Metadata
            # -------------------------------------------------

            st.caption(
                f"📍 {row['city'].title()} • "
                f"📅 {row['date'].strftime('%d %b %Y')}"
            )

            if "genre" in row.index:
                st.markdown(
                    f"**🎵 {row['genre'].title()}**"
                )

            # -------------------------------------------------
            # Similarity
            # -------------------------------------------------

            if "similarity" in row.index:

                st.caption("Match")

                st.progress(
                    min(
                        float(row["similarity"]),
                        1.0,
                    )
                )

            # -------------------------------------------------
            # Ticket Button
            # -------------------------------------------------

            if "url" in row.index:

                st.link_button(
                    "🎟 Buy Tickets",
                    row["url"],
                    width="stretch",
                )