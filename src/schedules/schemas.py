import enum
from typing import Optional

from src.schemas import TimedBaseScheme, BaseScheme


class Schedule_Type(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class ScheduleBase(BaseScheme):
    name: str
    description: Optional[str] = None
    schedule_type: Optional[Schedule_Type] = None


class ScheduleCreate(ScheduleBase):
    owner_id: int


class ScheduleRead(ScheduleBase, TimedBaseScheme):
    id: int


from src.users.schemas import UserRead


class ScheduleWithOwnerRead(ScheduleRead, TimedBaseScheme):
    owner: 'UserRead'
