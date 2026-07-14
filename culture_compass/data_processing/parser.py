import pandas as pd


def parse_events(response: dict) -> pd.DataFrame:
    """
    Parse Ticketmaster API response into a DataFrame.
    """

    events = response.get("_embedded", {}).get("events", [])

    rows = []

    for event in events:

        venue = event.get(
            "_embedded",
            {},
        ).get(
            "venues",
            [{}],
        )[0]

        classification = event.get(
            "classifications",
            [{}],
        )[0]

        # ----------------------------------------
        # Get highest resolution event image
        # ----------------------------------------

        images = event.get("images", [])

        image_url = None

        if images:

            best_image = max(
                images,
                key=lambda img: img.get("width", 0)
                * img.get("height", 0),
            )

            image_url = best_image.get("url")

        rows.append(
            {
                "event_id": event.get("id"),
                "event_name": event.get("name"),
                "genre": classification.get("genre", {}).get("name"),
                "segment": classification.get("segment", {}).get("name"),
                "date": event.get("dates", {})
                             .get("start", {})
                             .get("localDate"),
                "time": event.get("dates", {})
                             .get("start", {})
                             .get("localTime"),
                "city": venue.get("city", {}).get("name"),
                "country": venue.get("country", {}).get("name"),
                "venue_id": venue.get("id"),
                "latitude": venue.get("location", {}).get("latitude"),
                "longitude": venue.get("location", {}).get("longitude"),
                "url": event.get("url"),
                "image_url": image_url,
            }
        )

    return pd.DataFrame(rows)