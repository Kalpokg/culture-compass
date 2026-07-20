from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .city import City

from culture_compass.database.base import Base


class Country(Base):
    cities: Mapped[list["City"]] = relationship(
    back_populates="country",
    cascade="all, delete-orphan",
     )
    """
    Represents a country where events take place.
    """

    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    iso_code: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    def __repr__(self) -> str:

        return (
            f"Country(id={self.id}, "
            f"name='{self.name}')"
        )