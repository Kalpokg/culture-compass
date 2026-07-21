from sqlalchemy import select
from datetime import date
from culture_compass.database.models import (
    City,
    Country,
    Event,
    Genre,
    Source,
    Venue,
)
from sqlalchemy.orm import joinedload
from culture_compass.database.session import get_session
from culture_compass.models.canonical_event import CanonicalEvent
from culture_compass.utils.logger import logger


class EventRepository:
    """
    Handles persistence of canonical events.
    """

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def save(
        self,
        event: CanonicalEvent,
    ) -> None:
        """
        Save a single event.
        """

        with get_session() as session:
            self._save(
                session,
                event,
            )

    def save_many(self, events):
        inserted = 0
        skipped = 0

        with get_session() as session:
             for event in events:
                 try:
                    if self._save(session, event):
                       inserted += 1

                 except ValueError as e:
                     logger.warning(
                       "Skipping event '%s': %s",
                       event.event_name,
                      e,
                      )
                     skipped += 1
                     session.rollback()

                 except Exception:
                    session.rollback()
                    raise

             

        logger.info(
            "Finished batch. Inserted: %d | Skipped: %d",
             inserted,
             skipped,
        )

        return inserted

    # ---------------------------------------------------------
    # Internal save
    # ---------------------------------------------------------

    def _save(
        self,
        session,
        event: CanonicalEvent,
    ) -> bool:

        source = self._resolve_source(
            session,
            event.source,
        )

        country = self._resolve_country(
            session,
            event.country,
        )

        logger.warning(
         "Event=%r | city=%r | country=%r | venue=%r",
          event.event_name,
          event.city,
          event.country,
          event.venue_name,
        )

        logger.warning("Resolved country: %r", country)

        city = self._resolve_city(
            session,
            event.city,
            country,
        )

        venue = self._resolve_venue(
            session,
            event,
            city,
        )

        if venue is None:
            raise ValueError(
                "Unable to resolve venue."
            )

        genre = self._resolve_genre(
            session,
            event.genre,
            event.segment,
        )

        return self._create_event(
            session,
            event,
            source,
            venue,
            genre,
        )

    # ---------------------------------------------------------
    # Resolve helpers
    # ---------------------------------------------------------

    def _resolve_source(
        self,
        session,
        source_name: str,
    ) -> Source:

        source = session.scalar(
            select(Source).where(
                Source.name == source_name
            )
        )

        if source is None:
            raise ValueError(
                f"Unknown source: {source_name}"
            )

        return source

    def _resolve_country(
        self,
        session,
        country_name: str | None,
    ) -> Country | None:

        if country_name is None:
            return None

        country = session.scalar(
            select(Country).where(
                Country.name == country_name
            )
        )

        if country is None:

            country = Country(
                name=country_name,
            )

            session.add(country)
            session.flush()

            logger.info(
                "Created country: %s",
                country.name,
            )

        return country

    def _resolve_city(
        self,
        session,
        city_name: str | None,
        country: Country | None,
    ) -> City | None:

        if city_name is None or country is None:
            return None

        city = session.scalar(
            select(City).where(
                City.name == city_name,
                City.country_id == country.id,
            )
        )

        if city is None:

            city = City(
                name=city_name,
                country_id=country.id,
            )

            session.add(city)
            session.flush()

            logger.info(
                "Created city: %s",
                city.name,
            )

        return city

    def _resolve_genre(
        self,
        session,
        genre_name: str | None,
        segment: str | None,
    ) -> Genre | None:

        if genre_name is None:
            return None

        genre = session.scalar(
            select(Genre).where(
                Genre.name == genre_name
            )
        )

        if genre is None:

            genre = Genre(
                name=genre_name,
                segment=segment,
            )

            session.add(genre)
            session.flush()

            logger.info(
                "Created genre: %s",
                genre.name,
            )

        return genre

    def _resolve_venue(
        self,
        session,
        event: CanonicalEvent,
        city: City | None,
    ) -> Venue | None:

        if city is None:
            return None

        venue = None

        if event.source_venue_id:

            venue = session.scalar(
                select(Venue).where(
                    Venue.source_venue_id
                    == event.source_venue_id
                )
            )

        elif event.venue_name:

            venue = session.scalar(
                select(Venue).where(
                    Venue.name == event.venue_name,
                    Venue.city_id == city.id,
                )
            )

        if venue is None:

            venue = Venue(
                source_venue_id=event.source_venue_id,
                name=event.venue_name,
                city_id=city.id,
                latitude=event.latitude,
                longitude=event.longitude,
            )

            session.add(venue)
            session.flush()

            logger.info(
                "Created venue: %s",
                venue.name,
            )

        return venue

    # ---------------------------------------------------------
    # Event creation
    # ---------------------------------------------------------

    def _create_event(
        self,
        session,
        event: CanonicalEvent,
        source: Source,
        venue: Venue,
        genre: Genre | None,
    ) -> bool:

        existing = session.scalar(
            select(Event).where(
                Event.source_id == source.id,
                Event.source_event_id == event.source_event_id,
            )
        )

        if existing:

            logger.info(
                "Skipping existing event: %s",
                event.event_name,
            )

            return False

        db_event = Event(
            source_id=source.id,
            venue_id=venue.id,
            genre_id=genre.id if genre else None,
            source_event_id=event.source_event_id,
            event_name=event.event_name,
            event_date=event.event_date,
            event_time=event.event_time,
            ticket_url=event.ticket_url,
            image_url=event.image_url,
        )

        session.add(db_event)
        session.flush()

        logger.info(
            "Inserted event: %s",
            db_event.event_name,
        )

        return True
    def search_events(
        self,
        *,
        text: str | None = None,
        city: str | None = None,
        country: str | None = None,
        genre: str | None = None,
        provider: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        limit: int = 20,
     ):
       """
       Search events using optional filters.
       """
       
       with get_session() as session:
           query = (
                    select(Event)
                    .join(Event.venue)
                    .join(Venue.city)
                    .join(City.country)
                    .join(Event.genre)
                    .join(Event.source)
                    .options(
                       joinedload(Event.venue)
                       .joinedload(Venue.city)
                       .joinedload(City.country),
                       joinedload(Event.genre),
                       joinedload(Event.source),
                    )
           )

           if text:
               query = query.where(Event.event_name.ilike(f"%{text}%"))

           if city:
               query = query.where(City.name.ilike(f"%{city}%"))

           if country:
               query = query.where(Country.name.ilike(f"%{country}%"))

           if genre:
               query = query.where(Genre.name.ilike(f"%{genre}%"))

           if provider:
               query = query.where(Source.name.ilike(f"%{provider}%"))

           if start_date:
               query = query.where(Event.event_date >= start_date)

           if end_date:
               query = query.where(Event.event_date <= end_date)

           results = session.execute(query.limit(limit)).scalars().all()

       return results
    
    def get_countries(self) -> list[str]:

        with get_session() as session:

             query = (
                    select(Country.name)
                    .order_by(Country.name)
              )

             return session.execute(query).scalars().all()
    
    def get_cities(
           self,
           country: str | None = None,
            ) -> list[str]:

        with get_session() as session:

             query = (
               select(City.name)
               .join(City.country)
             )

             if country:

                query = query.where(
                Country.name == country
               )

             query = (
                    query
                    .distinct()
                    .order_by(City.name)
              )

             return session.execute(query).scalars().all()
    
    def get_genres(self) -> list[str]:

        with get_session() as session:

             query = (
                  select(Genre.name)
                  .order_by(Genre.name)
              )

             return session.execute(query).scalars().all()
    
    def get_providers(self) -> list[str]:

        with get_session() as session:

             query = (
                   select(Source.name)
                   .order_by(Source.name)
            )

             return session.execute(query).scalars().all()
    

    def get_event(self, event_id: int) -> Event:
        with get_session() as session:

             query = (
                    select(Event)
                    .options(
                     joinedload(Event.venue)
                    .joinedload(Venue.city)
                    .joinedload(City.country),
                     joinedload(Event.genre),
                     joinedload(Event.source),
                   )
                   .where(Event.id == event_id)
                    )

             return session.execute(query).scalar_one_or_none()