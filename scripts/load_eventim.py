from culture_compass.etl.pipelines.eventim_pipeline import (
    EventimPipeline,
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


def load_eventim():
    pipeline = EventimPipeline()

    total_events = 0

    for country in COUNTRIES:
        country_total = 0

        for keyword in KEYWORDS:
            print(
                "\n"
                "========================================\n"
                f"Country : {country}\n"
                f"Keyword : {keyword}\n"
                "========================================"
            )

            count = pipeline.run(
                keyword=keyword,
                country_code=country,
                page_limit=None,
            )

            country_total += count
            total_events += count

            print(
                f"\nFinished {country} / {keyword}: "
                f"{count} events."
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
    load_eventim()