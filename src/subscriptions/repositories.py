from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ItemNotFoundByIdException
from src.repositories import BaseRepo
from src.subscriptions.models import Subscription
from src.subscriptions.schemas import SubscriptionCreate, Subscription_Type


class SubscriptionRepo(BaseRepo[Subscription, SubscriptionCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Subscription, SubscriptionCreate)

    async def get_subscriptions_by_schedule_id(self, schedule_id: int, page: int, size: int):
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

    async def get_subscriptions_by_subscriber_id(self,
                                                 subscriber_id: int,
                                                 page: int,
                                                 size: int,
                                                 subscription_type: Subscription_Type = None):
        offset_min = page * size
        offset_max = (page + 1) * size

        select_smth = (
            select(self.model).filter_by(
                subscriber_id=subscriber_id
            )
        )

        if subscription_type:
            select_smth = select_smth.filter_by(subscription_type=subscription_type)

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return []
        return result[offset_min:offset_max]

    async def get_subscription_count_by_subscriber_id(self, subscriber_id):
        select_smth = (
            select(self.model).filter_by(
                subscriber_id=subscriber_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return 0
        return len(result)

    async def get_subscription_count_by_schedule_id(self, schedule_id):
        select_smth = (
            select(self.model).filter_by(
                schedule_id=schedule_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return 0
        return len(result)

    async def get_subscription_count_by_owner_id(self, owner_id):
        select_smth = (
            select(self.model).filter_by(
                owner_id=owner_id
            )
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        if not result:
            return 0
        return len(result)
