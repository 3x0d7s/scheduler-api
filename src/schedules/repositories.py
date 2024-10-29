from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ItemNotFoundByIdException
from src.repositories import BaseRepo
from src.schedules.models import Schedule
from src.schedules.schemas import ScheduleCreate


class ScheduleRepo(BaseRepo[Schedule, ScheduleCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Schedule, ScheduleCreate)

    async def get_schedules_by_owner_id(self,
                                        owner_id: int,
                                        page: int,
                                        size: int):
        offset_min = page * size
        offset_max = (page + 1) * size

        select_smth = (
            select(self.model).filter_by(
                owner_id=owner_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            raise []
        response = result[offset_min:offset_max]

        return response

    async def get_schedule_count_by_owner_id(self, owner_id):
        select_smth = (
            select(self.model).filter_by(
                owner_id=owner_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return 0
        return len(result)
