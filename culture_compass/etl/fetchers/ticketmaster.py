import logging
from datetime import datetime

import requests

from culture_compass.config.settings import TICKETMASTER_API_KEY

logger = logging.getLogger(__name__)


class TicketmasterFetcher:
    """
    Fetch events from the Ticketmaster Discovery API.
    """

    BASE_URL = (
        "https://app.ticketmaster.com/discovery/v2/events.json"
    )

    def fetch(
        self,
        keyword: str | None,
        country_code: str,
        size: int = 50,
        max_pages: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> dict:
        """
        Fetch events across multiple pages.

        Parameters
        ----------
        keyword : str | None
            Search keyword. If None, fetch all events.
        country_code : str
            ISO country code.
        size : int
            Number of events per page.
        max_pages : int | None
            Maximum number of pages to fetch.
            If None, fetch all available pages.
        start_date : datetime | None
            Inclusive start of the search window.
        end_date : datetime | None
            Inclusive end of the search window.
        """

        all_events = []
        page = 0

        while True:

            params = {
                "apikey": TICKETMASTER_API_KEY,
                "countryCode": country_code,
                "size": size,
                "page": page,
            }

            if keyword:
                params["keyword"] = keyword

            if start_date:
                params["startDateTime"] = (
                    start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                )

            if end_date:
                params["endDateTime"] = (
                    end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                )

            logger.info(f"Fetching page {page + 1}")

            try:
                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30,
                )

                if not response.ok:
                    logger.error(
                        "Request failed on page %s",
                        page + 1,
                    )
                    logger.error(
                        "Status code: %s",
                        response.status_code,
                    )
                    logger.error(
                        "Response: %s",
                        response.text,
                    )
                    response.raise_for_status()

            except requests.RequestException:
                logger.warning(
                    "Stopping pagination after page %s.",
                    page,
                )
                break

            data = response.json()

            events = (
                data
                .get("_embedded", {})
                .get("events", [])
            )

            if not events:
                logger.info("No more events found.")
                break

            all_events.extend(events)

            page_info = data.get("page", {})
            total_pages = page_info.get(
                "totalPages",
                page + 1,
            )

            logger.info(
                "Retrieved %s events "
                "(Total collected: %s)",
                len(events),
                len(all_events),
            )

            page += 1

            if page >= total_pages:
                break

            if (
                max_pages is not None
                and page >= max_pages
            ):
                logger.info(
                    "Reached max_pages=%s",
                    max_pages,
                )
                break

        logger.info(
            "Finished fetching %s events.",
            len(all_events),
        )

        return {
            "_embedded": {
                "events": all_events,
            }
        }