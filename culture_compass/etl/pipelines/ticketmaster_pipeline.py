from datetime import datetime

from culture_compass.database.repositories.event_repository import (
    EventRepository,
)
from culture_compass.etl.fetchers.ticketmaster import (
    TicketmasterFetcher,
)
from culture_compass.etl.parsers.ticketmaster import parse


class TicketmasterPipeline:
    """
    End-to-end Ticketmaster ETL pipeline.
    """

    def __init__(self):

        self.fetcher = TicketmasterFetcher()
        self.repository = EventRepository()

    def run(
        self,
        keyword: str,
        country_code: str,
        size: int = 50,
        max_pages: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> int:

        response = self.fetcher.fetch(
            keyword=keyword,
            country_code=country_code,
            size=size,
            max_pages=max_pages,
            start_date=start_date,
            end_date=end_date,
        )

        events = parse(response)

        print(f"Parsed events: {len(events)}")

        self.repository.save_many(events)

        return len(events)