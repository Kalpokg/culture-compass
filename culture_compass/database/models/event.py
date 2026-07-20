from datetime import date
from datetime import datetime
from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from culture_compass.database.base import Base

if TYPE_CHECKING:
    from .genre import Genre
    from .source import Source
    from .venue import Venue


class Event(Base):
    """
    Cultural event.
    """

    __tablename__ = "events"

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "source_event_id",
            name="uq_source_event",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
    )

    venue_id: Mapped[int] = mapped_column(
        ForeignKey("venues.id"),
        nullable=False,
    )

    genre_id: Mapped[int] = mapped_column(
        ForeignKey("genres.id"),
        nullable=False,
    )

    source_event_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    event_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    event_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    event_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    ticket_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    source: Mapped["Source"] = relationship(
        back_populates="events",
    )

    venue: Mapped["Venue"] = relationship(
        back_populates="events",
    )

    genre: Mapped["Genre"] = relationship(
        back_populates="events",
    )

    def __repr__(self) -> str:
        return (
            f"Event(id={self.id}, "
            f"name='{self.event_name}')"
        )