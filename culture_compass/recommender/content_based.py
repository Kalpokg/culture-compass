import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    """
    TF-IDF based recommender for cultural events.
    """

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.df = None
        self.matrix = None

    def fit(
        self,
        df: pd.DataFrame,
    ):
        """
        Fit the recommender on the processed dataset.
        """

        self.df = df.copy()

        self.matrix = self.vectorizer.fit_transform(
            self.df["event_text"]
        )

    def get_event_details(
        self,
        event_id: str,
    ):
        """
        Return full information for one event.
        """

        return self.df[
            self.df["event_id"] == event_id
        ]

    def recommend_same_event_dates(
        self,
        event_name: str,
        event_id: str,
        top_n: int = 5,
    ):
        """
        Recommend other performances of the same event.
        """

        results = self.df[
            self.df["event_name"] == event_name
        ]

        # Remove the selected performance
        results = results[
            results["event_id"] != event_id
        ]

        results = (
            results
            .sort_values("date")
            .head(top_n)
            .reset_index(drop=True)
        )

        return results[
            [
                "event_name",
                "genre",
                "city",
                "date",
                "image_url",
                "url",
            ]
        ]

    def recommend_similar_events(
        self,
        event_id: str,
        top_n: int = 5,
    ):
        """
        Recommend similar events using TF-IDF.
        """

        matches = self.df[
            self.df["event_id"] == event_id
        ]

        if matches.empty:
            raise ValueError(
                f"Event '{event_id}' not found."
            )

        idx = matches.index[0]

        query_name = self.df.loc[
            idx,
            "event_name",
        ]

        similarities = cosine_similarity(
            self.matrix[idx],
            self.matrix,
        ).flatten()

        indices = similarities.argsort()[::-1]

        results = self.df.iloc[
            indices
        ].copy()

        results["similarity"] = similarities[
            indices
        ]

        # Remove the selected event
        results = results[
            results["event_id"] != event_id
        ]

        # Remove other performances of the same event
        results = results[
            results["event_name"] != query_name
        ]

        results = (
            results
            .head(top_n)
            .reset_index(drop=True)
        )

        return results[
            [
                "event_name",
                "genre",
                "city",
                "date",
                "image_url",
                "venue_id",
                "url",
                "similarity",
            ]
        ]