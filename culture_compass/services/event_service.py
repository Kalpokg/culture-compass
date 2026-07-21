from culture_compass.database.repositories.event_repository import EventRepository
from culture_compass.dto.event import EventDTO


class EventService:
    """
    Service layer for event-related business logic.
    """

    def __init__(self):
        self.repository = EventRepository()

    def search_events(self, **kwargs) -> list[EventDTO]:
        """
        Search events and convert database models into DTOs.
        """
        events = self.repository.search_events(**kwargs)

        return [self._to_dto(event) for event in events]

    def _to_dto(self, event) -> EventDTO:
        """
        Convert an Event ORM object into an EventDTO.
        """
        return EventDTO(
            id=event.id,
            source_event_id=event.source_event_id,
            event_name=event.event_name,
            venue=event.venue.name,
            city=event.venue.city.name,
            country=event.venue.city.country.name,
            genre=event.genre.name,
            provider=event.source.name,
            event_date=event.event_date,
            event_time=event.event_time,
            image_url=event.image_url,
            ticket_url=event.ticket_url,
            )
    
    def get_countries(self):
        return self.repository.get_countries()

    def get_cities(self, country=None):
        return self.repository.get_cities(country)

    def get_genres(self):
        return self.repository.get_genres()

    def get_providers(self):
        return self.repository.get_providers()
    
    def get_event(self, event_id: int) -> EventDTO | None:

        event = self.repository.get_event(event_id)

        if event is None:
            return None

        return self._to_dto(event)