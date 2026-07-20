from typing import TYPE_CHECKING

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from culture_compass.database.base import Base

if TYPE_CHECKING:
    from .city import City
    from .event import Event


class Venue(Base):
    """
    Represents a venue where events take place.
    """

    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    source_venue_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id"),
        nullable=False,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    city: Mapped["City"] = relationship(
        back_populates="venues",
    )

    events: Mapped[list["Event"]] = relationship(
        back_populates="venue",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Venue(id={self.id}, "
            f"name='{self.name}')"
        )