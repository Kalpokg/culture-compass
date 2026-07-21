from pyventim import EventimCategory, EventimMarket

CATEGORY_MAP = {
    "music": EventimCategory.CONCERTS,
    "sports": EventimCategory.SPORTS,
    "arts": EventimCategory.CULTURE,
    "theatre": EventimCategory.THEATRE_AND_SHOWS,
    "family": EventimCategory.FAMILY,
}

MARKET_MAP = {
    "DE": EventimMarket.GERMANY,
    "BE": EventimMarket.BELGIUM,
    "NL": EventimMarket.NETHERLANDS,
    "FR": EventimMarket.FRANCE,
}