import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingSearch:
    """
    Semantic search using Sentence Transformers.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):

        self.model = SentenceTransformer(model_name)

    def fit(
        self,
        df: pd.DataFrame,
    ):

        self.df = df.copy()

        self.embeddings = self.model.encode(
            self.df["event_text"].tolist(),
            show_progress_bar=True,
        )

    def search(
        self,
        query: str,
        top_n: int = 10,
    ):

        query_embedding = self.model.encode(
            [query]
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings,
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