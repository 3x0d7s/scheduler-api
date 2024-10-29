import datetime
import enum
from datetime import time
from typing import Optional

from src.schemas import TimedBaseScheme, BaseScheme


class DayOfWeek(enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class EventBase(BaseScheme):
    name: str
    description: Optional[str] = None
    day_of_week: DayOfWeek
    start_time: time
    end_time: time


class EventCreate(EventBase):
    schedule_id: int


class EventRead(EventBase, TimedBaseScheme):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


from src.schedules.schemas import ScheduleRead


class EventWithScheduleRead(EventRead):
    schedule: 'ScheduleRead'
