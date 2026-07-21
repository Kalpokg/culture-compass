from culture_compass.etl.fetchers.eventim import EventimFetcher
from culture_compass.etl.parsers.eventim import EventimParser
from culture_compass.database.repositories.event_repository import EventRepository
from culture_compass.utils.logger import logger
from datetime import date

class EventimPipeline:
    """
    ETL pipeline for Eventim events.
    """

    def __init__(self) -> None:
        self.fetcher = EventimFetcher()
        self.parser = EventimParser()
        self.repository = EventRepository()

    def run(
        self,
        *,
        keyword: str,
        country_code: str,
        page_limit: int = 1,
    ) -> int:
        """
        Fetch, parse and persist Eventim events.

        Returns:
            Number of events inserted into the database.
        """

        product_groups = self.fetcher.fetch(
            keyword=keyword,
            country_code=country_code,
            page_limit=page_limit,
        )

        events = self.parser.parse(
            product_groups,
            country_code=country_code,
        )

        today = date.today()

        events = [
           e
           for e in events
           if e.event_date is not None
           and e.event_date >= today
        ]

        inserted = self.repository.save_many(events)

        logger.info(
            "Eventim pipeline completed (%s/%s): %s events inserted.",
            country_code,
            keyword,
            inserted,
        )

        return inserted