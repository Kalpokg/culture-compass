from functools import lru_cache

import reverse_geocoder as rg


@lru_cache(maxsize=100000)
def _lookup_country(latitude: float, longitude: float) -> str | None:
    """
    Cached reverse geocoding lookup for a single coordinate.
    """
    try:
        result = rg.search((latitude, longitude))[0]
        return result["cc"].upper()
    except Exception:
        return None


def country_from_coordinates(latitude: float, longitude: float) -> str | None:
    """
    Return ISO-2 country code from latitude/longitude.

    Examples:
        DE
        NL
        BE
        FR
        AT
    """
    if latitude is None or longitude is None:
        return None

    # Reduce duplicate lookups caused by tiny floating-point differences
    latitude = round(latitude, 5)
    longitude = round(longitude, 5)

    return _lookup_country(latitude, longitude)


def countries_from_coordinates_batch(
    coordinates: list[tuple[float | None, float | None]],
) -> dict[tuple[float, float], str | None]:
    """
    Resolve many (latitude, longitude) pairs to ISO-2 country codes in a
    single batched reverse-geocoding call.

    Much faster than calling country_from_coordinates() once per point in
    a loop -- reverse_geocoder's batch search (mode=1, single process)
    does one nearest-neighbor query for many points instead of paying
    per-call overhead for each individual point.

    Returns a dict mapping (rounded_lat, rounded_lon) -> country code
    (or None if that pair couldn't be resolved / was missing).
    """
    cleaned: list[tuple[float, float]] = []
    seen: set[tuple[float, float]] = set()

    for lat, lon in coordinates:
        if lat is None or lon is None:
            continue
        key = (round(lat, 5), round(lon, 5))
        if key not in seen:
            seen.add(key)
            cleaned.append(key)

    results: dict[tuple[float, float], str | None] = {}

    if not cleaned:
        return results

    try:
        raw_results = rg.search(cleaned, mode=1)
    except Exception:
        # Fall back to per-point lookups if the batch call itself fails,
        # rather than losing country data for the whole batch.
        for key in cleaned:
            results[key] = _lookup_country(*key)
        return results

    for key, r in zip(cleaned, raw_results):
        try:
            results[key] = r["cc"].upper()
        except Exception:
            results[key] = None

    return results
