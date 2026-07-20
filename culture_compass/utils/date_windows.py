from calendar import monthrange
from collections.abc import Iterator
from datetime import datetime


def generate_monthly_windows(
    start: datetime,
    end: datetime,
) -> Iterator[tuple[datetime, datetime]]:
    """
    Yield monthly (start_date, end_date) windows between
    the given start and end datetimes.
    """

    current = start

    while current <= end:

        last_day = monthrange(
            current.year,
            current.month,
        )[1]

        window_end = datetime(
            current.year,
            current.month,
            last_day,
            23,
            59,
            59,
        )

        if window_end > end:
            window_end = end

        yield current, window_end

        if current.month == 12:
            current = datetime(
                current.year + 1,
                1,
                1,
            )
        else:
            current = datetime(
                current.year,
                current.month + 1,
                1,
            )