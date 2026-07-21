from dataclasses import dataclass
from datetime import date
from datetime import time


@dataclass(slots=True)
class EventDTO:
    """
    Data Transfer Object used by the UI.

    id:
        Internal database primary key.

    source_event_id:
        Original provider event ID
        (Ticketmaster/Eventim/etc.).
    """

    # Database IDs
    id: int
    source_event_id: str

    # Event information
    event_name: str

    # Location
    venue: str
    city: str
    country: str

    # Classification
    genre: str
    provider: str

    # Date & Time
    event_date: date
    event_time: time | None

    # Links
    image_url: str | None
    ticket_url: str | None