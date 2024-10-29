from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.events.models import Event
from src.events.schemas import EventCreate
from src.repositories import BaseRepo


class EventsRepo(BaseRepo[Event, EventCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Event, EventCreate)

    async def get_all_by_schedule_id(self, schedule_id: int, page: int, size: int):
        offset_min = page * size
        offset_max = (page + 1) * size

        select_smth = (
            select(self.model).filter_by(
                schedule_id=schedule_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return []
        return result[offset_min:offset_max]

    async def get_events_count_by_schedule_id(self, schedule_id: int):
        select_smth = (
            select(self.model).filter_by(
                schedule_id=schedule_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return 0
        return len(result)