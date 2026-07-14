from pathlib import Path
import json

import pandas as pd

from culture_compass.data_processing.parser import parse_events
from culture_compass.data_processing.cleaning import clean_events
from culture_compass.features.text_features import create_event_text


class DatasetBuilder:
    """
    Builds one processed dataset from all raw JSON files.
    """

    def __init__(self):

        self.raw_dir = Path("data/raw")
        self.processed_dir = Path("data/processed")

        self.processed_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def build(self):

        dataframes = []

        json_files = sorted(
            self.raw_dir.glob("*.json")
        )

        print(f"\nFound {len(json_files)} raw files.\n")

        for file in json_files:

            print(f"Processing {file.name}")

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                response = json.load(f)

            try:

                df = parse_events(response)

                if df.empty:
                    continue

                df = clean_events(df)

                df = create_event_text(df)

                dataframes.append(df)

            except Exception as e:

                print(
                    f"Skipping {file.name}: {e}"
                )

        if not dataframes:

            print("No events found.")

            return

        dataset = pd.concat(
            dataframes,
            ignore_index=True,
        )

        dataset.drop_duplicates(
            subset="event_id",
            inplace=True,
        )

        dataset.sort_values(
            by="date",
            inplace=True,
        )

        output = (
            self.processed_dir
            / "events.parquet"
        )

        dataset.to_parquet(
            output,
            index=False,
        )

        print("\nDataset Summary")
        print("--------------------")
        print(f"Events : {len(dataset)}")
        print(f"Columns: {len(dataset.columns)}")
        print(f"Saved  : {output}")

        return dataset