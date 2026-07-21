from culture_compass.config.eventim import CATEGORY_MAP, MARKET_MAP
from culture_compass.utils.logger import logger
from pyventim import EventimClient


class EventimFetcher:
    """
    Fetch raw Eventim product groups.

    This class is responsible only for communicating with the Eventim API.
    It returns raw EventimPublicProductGroup objects, leaving all parsing
    and normalization to the parser layer.
    """

    def fetch(
        self,
        *,
        keyword: str,
        country_code: str,
        page_limit: int = 1,
    ):

        try:
            category = CATEGORY_MAP[keyword.lower()]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported Eventim keyword: '{keyword}'."
            ) from exc

        try:
            market = MARKET_MAP[country_code.upper()]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported Eventim market: '{country_code}'."
            ) from exc

        logger.info(
            "Fetching Eventim product groups "
            "(country=%s, keyword=%s, page_limit=%s)",
            country_code,
            keyword,
            page_limit,
        )

        client = EventimClient(market)

        product_groups = list(
            client.product_groups(
                categories=[category],
                page_limit=page_limit,
            )
        )

        logger.info(
            "Retrieved %s Eventim product groups.",
            len(product_groups),
        )

        return product_groups