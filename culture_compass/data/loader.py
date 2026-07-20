from culture_compass.data.database_loader import load_from_database
from culture_compass.features.text_features import create_event_text

import pandas as pd


def load_dataset():
    df = load_from_database()

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    df = create_event_text(df)

    return df