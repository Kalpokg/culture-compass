from datetime import datetime

from culture_compass.etl.pipelines.ticketmaster_pipeline import (
    TicketmasterPipeline,
)
from culture_compass.utils.date_windows import (
    generate_monthly_windows,
)

COUNTRIES = [
    "DE",  # Germany
    "FR",  # France
    "NL",  # Netherlands
    "BE",  # Belgium
]

KEYWORDS = [
    "music",
    "sports",
    "arts",
    "theatre",
    "family",
]


def main():

    pipeline = TicketmasterPipeline()

    current_year = datetime.now().year

    total_events = 0

    windows = list(
        generate_monthly_windows(
            start=datetime(current_year, 1, 1),
            end=datetime(
                current_year,
                12,
                31,
                23,
                59,
                59,
            ),
        )
    )

    for country in COUNTRIES:

        country_total = 0

        for keyword in KEYWORDS:

            keyword_total = 0

            for start_date, end_date in windows:

                print(
                    "\n"
                    "========================================\n"
                    f"Country : {country}\n"
                    f"Keyword : {keyword}\n"
                    f"Window  : "
                    f"{start_date:%Y-%m-%d} "
                    f"to "
                    f"{end_date:%Y-%m-%d}\n"
                    "========================================"
                )

                count = pipeline.run(
                    keyword=keyword,
                    country_code=country,
                    size=50,
                    max_pages=None,
                    start_date=start_date,
                    end_date=end_date,
                )

                keyword_total += count
                country_total += count
                total_events += count

            print(
                f"\nFinished {country} / {keyword}: "
                f"{keyword_total} events."
            )

        print(
            f"\nFinished country {country}: "
            f"{country_total} events."
        )

    print(
        "\n"
        "========================================\n"
        f"Finished loading {total_events} events.\n"
        "========================================"
    )


if __name__ == "__main__":
    main()