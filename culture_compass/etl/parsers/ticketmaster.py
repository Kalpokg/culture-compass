from datetime import date, time

from culture_compass.models.canonical_event import CanonicalEvent


def parse(response: dict) -> list[CanonicalEvent]:
    """
    Parse a Ticketmaster API response into CanonicalEvent objects.
    """

    raw_events = response.get(
        "_embedded",
        {},
    ).get(
        "events",
        [],
    )

    events: list[CanonicalEvent] = []

    for event in raw_events:

        venue = (
            event.get("_embedded", {})
            .get("venues", [{}])[0]
        )

        classification = event.get(
            "classifications",
            [{}],
        )[0]

        # -----------------------------------------
        # Classification
        # -----------------------------------------

        genre = (
            classification.get("genre", {})
            .get("name")
            or "Unknown"
        )

        segment = (
            classification.get("segment", {})
            .get("name")
            or "Unknown"
        )

        # -----------------------------------------
        # Highest resolution image
        # -----------------------------------------

        images = event.get("images", [])

        image_url = None

        if images:

            best_image = max(
                images,
                key=lambda img: (
                    img.get("width", 0)
                    * img.get("height", 0)
                ),
            )

            image_url = best_image.get("url")

        # -----------------------------------------
        # Parse date
        # -----------------------------------------

        event_date = None

        local_date = (
            event.get("dates", {})
            .get("start", {})
            .get("localDate")
        )

        if local_date:

            event_date = date.fromisoformat(
                local_date
            )

        # -----------------------------------------
        # Parse time
        # -----------------------------------------

        event_time = None

        local_time = (
            event.get("dates", {})
            .get("start", {})
            .get("localTime")
        )

        if local_time:

            event_time = time.fromisoformat(
                local_time
            )

        # -----------------------------------------
        # Canonical event
        # -----------------------------------------

        events.append(
            CanonicalEvent(
                source="Ticketmaster",

                source_event_id=event.get("id"),

                source_venue_id=venue.get("id"),

                event_name=event.get("name"),

                genre=genre,

                segment=segment,

                venue_name=venue.get("name"),

                city=venue.get(
                    "city",
                    {},
                ).get("name"),

                country=venue.get(
                    "country",
                    {},
                ).get("name"),

                latitude=float(
                    venue.get(
                        "location",
                        {},
                    ).get("latitude")
                )
                if venue.get(
                    "location",
                    {},
                ).get("latitude")
                else None,

                longitude=float(
                    venue.get(
                        "location",
                        {},
                    ).get("longitude")
                )
                if venue.get(
                    "location",
                    {},
                ).get("longitude")
                else None,

                event_date=event_date,

                event_time=event_time,

                ticket_url=event.get("url"),

                image_url=image_url,
            )
        )

    return events