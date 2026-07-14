import pandas as pd


def create_event_text(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["event_text"] = (
        df["event_name"].fillna("")
        + " "
        + df["genre"].fillna("")
        + " "
        + df["segment"].fillna("")
        + " "
        + df["city"].fillna("")
    )

    return df