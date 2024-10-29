from datetime import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.events.schemas import DayOfWeek
from src.models import TimedBaseModel


class Event(TimedBaseModel):
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    day_of_week: Mapped["DayOfWeek"] = mapped_column(nullable=False)
    start_time: Mapped[time] = mapped_column(nullable=False)
    end_time: Mapped[time] = mapped_column(nullable=False)

    schedule: Mapped["Schedule"] = relationship(back_populates="events", lazy="selectin")
