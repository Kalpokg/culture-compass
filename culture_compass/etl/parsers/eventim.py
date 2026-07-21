from __future__ import annotations

from datetime import datetime
from culture_compass.utils.country import normalize_country
from culture_compass.models.canonical_event import CanonicalEvent
from culture_compass.utils.logger import logger


class EventimParser:
    """
    Convert raw Eventim product groups into CanonicalEvent objects.
    """

    SOURCE_NAME = "Eventim"

    def parse(
        self,
        product_groups: list,
        *,
        country_code: str,
    ) -> list[CanonicalEvent]:
        """
        Parse Eventim product groups into canonical events.

        Each ProductGroup may contain multiple Products.
        Each Product becomes one CanonicalEvent.
        """

        events: list[CanonicalEvent] = []

        for group in product_groups:

            categories = group.categories or []

            segment = (
                categories[0]["name"]
                if len(categories) > 0
                else "Unknown"
            )

            if len(categories) >= 2:
               segment = categories[0]["name"]
               genre = categories[1]["name"]
            elif len(categories) == 1:
               segment = categories[0]["name"]
               genre = categories[0]["name"]
            else:
               segment = "Unknown"
               genre = "Unknown"

            image_url = group.image_url

            for product in group.products:

                live = (
                    product.type_attributes.get("liveEntertainment", {})
                    if product.type_attributes
                    else {}
                )

                location = live.get("location", {})

                geo = location.get("geoLocation", {})

                start_date = live.get("startDate")

                event_datetime = (
                    datetime.fromisoformat(start_date)
                    if start_date
                    else None
                )

                event = CanonicalEvent(
                    source=self.SOURCE_NAME,
                    source_event_id=str(product.product_id),
                    event_name=product.name,
                    event_date=event_datetime.date()
                    if event_datetime
                    else None,
                    event_time=event_datetime.time()
                    if event_datetime
                    else None,
                    venue_name=location.get("name"),
                    city=location.get("city"),
                    country=normalize_country(country_code),
                    latitude=geo.get("latitude"),
                    longitude=geo.get("longitude"),
                    genre=genre,
                    segment=segment,
                    image_url=image_url,
                    ticket_url=product.link,
                    source_venue_id=None
                )

                events.append(event)

        logger.info(
            "Parsed %s canonical events from %s Eventim product groups.",
            len(events),
            len(product_groups),
        )

        return events