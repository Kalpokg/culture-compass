from __future__ import annotations

from datetime import datetime
from pprint import pprint

from culture_compass.models.canonical_event import CanonicalEvent
from culture_compass.utils.country import normalize_country
from culture_compass.utils.geocode import countries_from_coordinates_batch
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

        # -------------------------------------------------------------
        # Pass 1: walk all product groups, build raw per-event data,
        # and collect every (lat, lon) pair we'll need to geocode.
        # -------------------------------------------------------------
        raw_items = []
        coordinates: list[tuple[float | None, float | None]] = []

        for group in product_groups:

            categories = group.categories or []

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

                city = location.get("city")
                latitude = geo.get("latitude")
                longitude = geo.get("longitude")

                start_date = live.get("startDate")

                event_datetime = (
                    datetime.fromisoformat(start_date)
                    if start_date
                    else None
                )

                coordinates.append((latitude, longitude))

                raw_items.append(
                    {
                        "product": product,
                        "location": location,
                        "city": city,
                        "latitude": latitude,
                        "longitude": longitude,
                        "event_datetime": event_datetime,
                        "genre": genre,
                        "segment": segment,
                        "image_url": image_url,
                    }
                )

        # -------------------------------------------------------------
        # Pass 2: one batched geocoding call for every unique
        # coordinate pair collected above.
        # -------------------------------------------------------------
        geocoded = countries_from_coordinates_batch(coordinates)

        # -------------------------------------------------------------
        # Pass 3: build the actual CanonicalEvent objects, looking up
        # each event's country from the batch result instead of
        # geocoding one at a time.
        # -------------------------------------------------------------
        events: list[CanonicalEvent] = []

        for item in raw_items:

            product = item["product"]
            location = item["location"]
            city = item["city"]
            latitude = item["latitude"]
            longitude = item["longitude"]
            event_datetime = item["event_datetime"]

            key = (
                (round(latitude, 5), round(longitude, 5))
                if latitude is not None and longitude is not None
                else None
            )
            detected_country = geocoded.get(key) if key else None

            country = normalize_country(
                detected_country or country_code
            )

            SUPPORTED_COUNTRIES = {"DE", "FR", "NL", "BE"}

            if country not in SUPPORTED_COUNTRIES:
                continue

            # --------------------------------------------------
            # DEBUG
            # --------------------------------------------------
            if city in {
                "Amsterdam",
                "Rotterdam",
                "Leiden",
                "Antwerp",
                "Brussels",
                "Cologne",
                "Bonn",
                "Wien",
                "Vienna",
            }:
                print("\n" + "=" * 80)
                print(f"SEARCH COUNTRY    : {country_code}")
                print(f"DETECTED COUNTRY : {detected_country}")
                print(f"FINAL COUNTRY    : {country}")
                print(f"CITY             : {city}")
                print("LOCATION:")
                pprint(location)
                print("=" * 80 + "\n")
            # --------------------------------------------------

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
                city=city,
                country=country,
                latitude=latitude,
                longitude=longitude,
                genre=item["genre"],
                segment=item["segment"],
                image_url=item["image_url"],
                ticket_url=product.link,
                source_venue_id=None,
            )

            events.append(event)

        logger.info(
            "Parsed %s canonical events from %s Eventim product groups.",
            len(events),
            len(product_groups),
        )

        return events
