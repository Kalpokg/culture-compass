from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .event import Event
from culture_compass.database.base import Base


class Source(Base):
    events: Mapped[list["Event"]] = relationship(
    back_populates="source",
    cascade="all, delete-orphan",
     )
    """
    Event data provider.
    """

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    def __repr__(self) -> str:

        return (
            f"Source(id={self.id}, "
            f"name='{self.name}')"
        )