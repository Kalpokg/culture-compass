from culture_compass.database.repositories.event_repository import (
    EventRepository,
)
from culture_compass.database.session import get_session


def main():

    repository = EventRepository()

    with get_session() as session:

        source = repository._resolve_source(
            session,
            "Ticketmaster",
        )

        print(source)


if __name__ == "__main__":
    main()