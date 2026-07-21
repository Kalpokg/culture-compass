# culture_compass/utils/country.py

COUNTRY_MAP = {
    "Germany": "DE",
    "DE": "DE",
    "France": "FR",
    "FR": "FR",
    "Belgium": "BE",
    "BE": "BE",
    "Netherlands": "NL",
    "NL": "NL",
}

def normalize_country(country: str | None) -> str | None:
    if country is None:
        return None
    return COUNTRY_MAP.get(country.strip(), country.strip())