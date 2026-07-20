from dataclasses import dataclass
from datetime import date, time


@dataclass(slots=True)
class CanonicalEvent:
    """
    Standard event representation used throughout the ETL pipeline.
    """

    source: str

    source_event_id: str
    source_venue_id: str | None

    event_name: str

    genre: str | None
    segment: str | None

    venue_name: str | None
    city: str | None
    country: str | None

    latitude: float | None
    longitude: float | None

    event_date: date | None
    event_time: time | None

    ticket_url: str | None
    image_url: str | None