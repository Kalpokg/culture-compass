import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearch:
    """
    TF-IDF based semantic search over events.
    """

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

    def fit(
        self,
        df: pd.DataFrame,
    ):

        self.df = df.copy()

        self.matrix = self.vectorizer.fit_transform(
            self.df["event_text"]
        )

    def search(
        self,
        query: str,
        top_n: int = 10,
    ):

        query_vector = self.vectorizer.transform(
            [query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.matrix,
        ).flatten()

        indices = similarities.argsort()[::-1]

        results = self.df.iloc[
            indices
        ].copy()

        results["score"] = similarities[
            indices
        ]

        return (
            results[
                [
                    "event_name",
                    "genre",
                    "city",
                    "date",
                    "score",
                ]
            ]
            .head(top_n)
            .reset_index(drop=True)
        )