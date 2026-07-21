from sqlalchemy import select

from culture_compass.database.models import Source
from culture_compass.database.session import get_session


SOURCES = [
    {
        "name": "Ticketmaster",
        "website": "https://developer.ticketmaster.com/",
    },
    {
        "name": "Eventim",
        "website": "https://www.eventim.com/",
    },
]


def seed_sources():

    with get_session() as session:

        for source in SOURCES:

            exists = session.scalar(
                select(Source).where(
                    Source.name == source["name"]
                )
            )

            if exists is None:

                session.add(
                    Source(
                        name=source["name"],
                        website=source["website"],
                    )
                )

                print(f"✓ Added {source['name']}")

            else:

                print(f"✓ {source['name']} already exists")


def main():

    seed_sources()

    print("Database seeded.")


if __name__ == "__main__":
    main()