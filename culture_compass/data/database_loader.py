import pandas as pd

from sqlalchemy.orm import joinedload

from culture_compass.database.models.city import City
from culture_compass.database.models.event import Event
from culture_compass.database.models.venue import Venue
from culture_compass.database.session import get_session


def load_from_database() -> pd.DataFrame:
    """
    Load all events from PostgreSQL into a pandas DataFrame.
    """

    with get_session() as session:

        events = (
            session.query(Event)
            .options(
                joinedload(Event.genre),
                joinedload(Event.venue)
                .joinedload(Venue.city)
                .joinedload(City.country),
            )
            .all()
        )

        rows = []

        for event in events:
            rows.append(
                {
                    "event_id": event.source_event_id,
                    "event_name": event.event_name,
                    "genre": event.genre.name,
                    "segment": event.genre.segment,
                    "city": event.venue.city.name,
                    "country": event.venue.city.country.name,
                    "venue_name": event.venue.name,
                    "latitude": event.venue.latitude,
                    "longitude": event.venue.longitude,
                    "date": event.event_date,
                    "time": event.event_time,
                    "url": event.ticket_url,
                    "venue_id": event.venue.id,
                    "image_url": event.image_url,
                }
            )

    df = pd.DataFrame(rows)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df