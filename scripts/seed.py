from sqlalchemy import select

from culture_compass.database.models import Source
from culture_compass.database.session import get_session


def seed_sources():

    with get_session() as session:

        exists = session.scalar(
            select(Source).where(
                Source.name == "Ticketmaster"
            )
        )

        if exists is None:

            session.add(
                Source(
                    name="Ticketmaster",
                    website="https://developer.ticketmaster.com/",
                )
            )

            print("✓ Added Ticketmaster")

        else:

            print("✓ Ticketmaster already exists")


def main():

    seed_sources()

    print("Database seeded.")


if __name__ == "__main__":
    main()