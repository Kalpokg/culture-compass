from sqlalchemy import text

from culture_compass.database.session import engine


def main():

    with engine.connect() as connection:

        version = connection.execute(
            text("SELECT version();")
        )

        print(version.scalar())


if __name__ == "__main__":
    main()