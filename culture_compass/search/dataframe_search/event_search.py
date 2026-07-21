import pandas as pd


class EventSearch:
    """
    Search events using optional filters.
    """

    def __init__(
        self,
        df: pd.DataFrame,
    ):

        self.df = df

    def search(
        self,
        query: str | None = None,
        city: str | None = None,
        genre: str | None = None,
        country: str | None = None,
        start_date=None,
        end_date=None,
        top_n: int = 20,
    ):
        """
        Search events using optional filters.

        Parameters
        ----------
        query : str, optional
            Keyword to search in event names.
        city : str, optional
            Filter by city.
        genre : str, optional
            Filter by genre.
        country : str, optional
            Filter by country.
        start_date : datetime-like, optional
            Return events on or after this date.
        end_date : datetime-like, optional
            Return events on or before this date.
        top_n : int
            Maximum number of results.
        """

        results = self.df.copy()

        # Keyword search
        if query:

            results = results[
                results["event_name"]
                .str.contains(
                    query,
                    case=False,
                    na=False,
                )
            ]

        # City filter
        if city:

            results = results[
                results["city"]
                .str.lower()
                == city.lower()
            ]

        # Genre filter
        if genre:

            results = results[
                results["genre"]
                .str.lower()
                == genre.lower()
            ]

        # Country filter
        if country:

            results = results[
                results["country"]
                .str.lower()
                == country.lower()
            ]

        # Date filters
        if start_date is not None:

            results = results[
                results["date"] >= start_date
            ]

        if end_date is not None:

            results = results[
                results["date"] <= end_date
            ]

        # Sort by date
        results = results.sort_values("date")

        # Keep only useful columns
        results = results[
            [
                "event_id",
                "event_name",
                "genre",
                "city",
                "country",
                "date",
                "url",
            ]
        ]

        return results.head(top_n).reset_index(drop=True)