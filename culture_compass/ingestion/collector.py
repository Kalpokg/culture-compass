from datetime import datetime
from pathlib import Path
import csv
import json

from culture_compass.api.ticketmaster_client import TicketmasterClient
from culture_compass.config.collector_config import (
    CITIES,
    KEYWORDS,
    MAX_PAGES,
)


class EventCollector:
    """
    Collects event data from Ticketmaster and stores
    raw JSON files together with ingestion metadata.
    """

    def __init__(self):
        self.client = TicketmasterClient()

        self.raw_dir = Path("data/raw")
        self.metadata_dir = Path("data/metadata")

        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.metadata_dir / "ingestion_log.csv"

        self._initialize_metadata()

    def _initialize_metadata(self):
        """
        Create the metadata CSV if it doesn't exist.
        """

        if self.metadata_file.exists():
            return

        with open(self.metadata_file, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "collected_at",
                    "city",
                    "keyword",
                    "page",
                    "filename",
                    "event_count",
                    "status",
                ]
            )

    def _generate_filename(
        self,
        city: str,
        keyword: str,
        page: int,
    ) -> str:
        """
        Generate a unique filename.
        """

        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")

        city = city.lower().replace(" ", "_")
        keyword = keyword.lower().replace(" ", "_")

        return (
            f"{timestamp}_{city}_{keyword}_page{page}.json"
        )

    def _save_json(
        self,
        response: dict,
        filename: str,
    ) -> Path:
        """
        Save the raw API response.
        """

        filepath = self.raw_dir / filename

        with open(filepath, "w", encoding="utf-8") as file:

            json.dump(
                response,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return filepath

    def _count_events(self, response: dict) -> int:
        """
        Count returned events.
        """

        return len(
            response.get("_embedded", {}).get("events", [])
        )

    def _write_metadata(
        self,
        city: str,
        keyword: str,
        page: int,
        filename: str,
        event_count: int,
        status: str,
    ):
        """
        Append one ingestion record.
        """

        with open(
            self.metadata_file,
            "a",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    datetime.now().isoformat(timespec="seconds"),
                    city,
                    keyword,
                    page,
                    filename,
                    event_count,
                    status,
                ]
            )

    def collect(
        self,
        keyword: str,
        city: str,
        page: int = 0,
    ) -> Path:
        """
        Collect one page of events.
        """

        try:

            response = self.client.search_events(
                keyword=keyword,
                city=city,
                page=page,
            )

            filename = self._generate_filename(
                city=city,
                keyword=keyword,
                page=page,
            )

            filepath = self._save_json(
                response=response,
                filename=filename,
            )

            event_count = self._count_events(response)

            self._write_metadata(
                city=city,
                keyword=keyword,
                page=page,
                filename=filename,
                event_count=event_count,
                status="success",
            )

            return filepath

        except Exception:

            self._write_metadata(
                city=city,
                keyword=keyword,
                page=page,
                filename="",
                event_count=0,
                status="failed",
            )

            raise

    def collect_dataset(self):
        """
        Collect all configured cities, keywords and pages.
        """

        total_requests = (
            len(CITIES)
            * len(KEYWORDS)
            * MAX_PAGES
        )

        current_request = 1

        for city in CITIES:

            for keyword in KEYWORDS:

                for page in range(MAX_PAGES):

                    print(
                        f"[{current_request}/{total_requests}] "
                        f"{city:<12} | "
                        f"{keyword:<15} | "
                        f"Page {page}"
                    )

                    try:

                        self.collect(
                            city=city,
                            keyword=keyword,
                            page=page,
                        )

                    except Exception as e:

                        print(f"❌ Failed: {e}")

                    current_request += 1

        print("\n✅ Dataset collection complete.")