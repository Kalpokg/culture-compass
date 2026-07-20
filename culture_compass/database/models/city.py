from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from culture_compass.database.base import Base

if TYPE_CHECKING:
    from .country import Country
    from .venue import Venue


class City(Base):
    """
    Represents a city where events take place.
    """

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        back_populates="cities",
    )

    venues: Mapped[list["Venue"]] = relationship(
        back_populates="city",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"City(id={self.id}, "
            f"name='{self.name}')"
        )