from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import TimedBaseModel
from src.schedules.schemas import Schedule_Type


class Schedule(TimedBaseModel):
    name:           Mapped[str] = mapped_column(nullable=False)
    description:    Mapped[str] = mapped_column(nullable=True)
    owner_id:       Mapped[int] = mapped_column(ForeignKey("user.id"))
    schedule_type:  Mapped["Schedule_Type"] = mapped_column(nullable=False, default=Schedule_Type.PRIVATE)

    owner:          Mapped["User"] = relationship(back_populates="schedules")

    events:         Mapped[List["Event"]] = relationship(
        back_populates="schedule",
        lazy="selectin",
        cascade="all, delete-orphan"
    )

    subscribers: Mapped[List["User"]] = relationship(
        secondary="subscription",
        back_populates="subscriptions",
        lazy="selectin"
    )

    subscription_associations: Mapped[List["Subscription"]] = relationship(
        back_populates="schedule",
        cascade="all, delete-orphan"
    )
