import pandas as pd


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the events dataframe.
    """

    df = df.copy()

    # Remove duplicate events
    df = df.drop_duplicates(subset="event_id")

    # Convert date column
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    # Convert coordinates to numeric
    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce",
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce",
    )

    # Normalize text columns
    text_columns = [
        "event_name",
        "genre",
        "segment",
        "city",
        "country",
    ]

    for col in text_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.lower()
            )

    return df