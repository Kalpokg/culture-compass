from pathlib import Path

import pandas as pd


def load_dataset():

    filepath = Path("data/processed/events.parquet")  # use your actual filename

    df = pd.read_parquet(filepath)

    # Convert after loading
    df["date"] = pd.to_datetime(df["date"])

    return df