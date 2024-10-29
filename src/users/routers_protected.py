import math

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.dependencies import PaginationParams, get_pagination_params
from src.exceptions import ItemNotFoundByIdException
from src.responses import paginated_response_content
from src.schedules.repositories import ScheduleRepo
from src.schedules.schemas import ScheduleRead, ScheduleCreate, ScheduleBase, Schedule_Type
from src.schemas import PaginatedResponseScheme
from src.setup import get_async_session
from src.subscriptions.repositories import SubscriptionRepo
from src.subscriptions.schemas import Subscription_Type, SubscriptionScheduleRead, SubscriptionCreate
from src.users.models import User

router = APIRouter(
    prefix="/me",
    tags=["user_authorized"]
)

current_user = fastapi_users.current_user()


@router.get("/schedules", response_model=PaginatedResponseScheme[ScheduleRead])
async def get_owned_schedules_as_authorized(session: AsyncSession = Depends(get_async_session),
                                            user: User = Depends(current_user),
                                            pagination_params: PaginationParams = Depends(get_pagination_params)):
    repo = ScheduleRepo(session)

    count = await repo.get_count()
    result = await repo.get_schedules_by_owner_id(owner_id=user.id, 
                                                  page=pagination_params.page, 
                                                  size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/subscriptions/as_{subscription_type}", response_model=PaginatedResponseScheme[SubscriptionScheduleRead])
async def get_subscriptions_by_its_type_as_authorized(session: AsyncSession = Depends(get_async_session),
                                                      user: User = Depends(current_user),
                                                      subscription_type: Subscription_Type =
                                                        Subscription_Type.FOLLOWER,
                                                      pagination_params: PaginationParams = Depends(get_pagination_params)):
    repo = SubscriptionRepo(session)

    subscription_count = await repo.get_subscription_count_by_subscriber_id(subscriber_id=user.id)

    try:
        result = await repo.get_subscriptions_by_subscriber_id(subscriber_id=user.id,
                                                               page=pagination_params.page,
                                                               size=pagination_params.size,
                                                               subscription_type=subscription_type)
    except ItemNotFoundByIdException:
        result = []

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      subscription_count)
    


@router.post("/subscriptions/add_as_follower/{schedule_id}")
async def subscribe(schedule_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    schedule_repo = ScheduleRepo(session)

    schedule = await schedule_repo.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    if schedule.owner_id == user.id:
        raise HTTPException(status_code=403, detail="You can't subscribe to your own schedule")

    if schedule.schedule_type == Schedule_Type.PRIVATE:
        raise HTTPException(status_code=403, detail="You can't subscribe to private schedules")

    repo = SubscriptionRepo(session)

    new_subscription = SubscriptionCreate(
        subscriber_id=user.id,
        schedule_id=schedule_id,
        subscription_type=Subscription_Type.FOLLOWER
    )

    await repo.create(new_subscription)
    return {"status": "success"}


@router.delete("/schedules/{schedule_id}")
async def delete_owned_schedule_as_authorized(schedule_id: int,
                                              session: AsyncSession = Depends(get_async_session),
                                              user: User = Depends(current_user)):
    repo = ScheduleRepo(session)

    schedule = await repo.get_by_id(schedule_id)
    if schedule and schedule.owner_id == user.id:
        await repo.delete_by_id(schedule_id)
        return {"status": "success"}

    return {"status": "fail"}

@router.delete("/subscriptions/{subscription_id}")
async def delete_subscription_as_authorized(subscription_id: int,
                                              session: AsyncSession = Depends(get_async_session),
                                              user: User = Depends(current_user)):
    repo = SubscriptionRepo(session)

    subscription = await repo.get_by_id(subscription_id)
    if subscription and subscription.subscriber_id == user.id:
        await repo.delete_by_id(subscription_id)
        return {"status": "success"}

    return {"status": "fail"}

@router.post("/schedules")
async def create_owned_schedule_as_authorized(new_schedule: ScheduleBase,
                                              session: AsyncSession = Depends(get_async_session),
                                              user: User = Depends(current_user)):
    try:
        schedule_repo = ScheduleRepo(session)
        subscription_repo = SubscriptionRepo(session)

        created_schedule = await schedule_repo.create(
            ScheduleCreate(**new_schedule.model_dump(), owner_id=user.id))

        new_subscription = SubscriptionCreate(
            subscriber_id=created_schedule.owner_id,
            schedule_id=created_schedule.id,
            subscription_type=Subscription_Type.OWNER
        )

        await subscription_repo.create(new_subscription)
        return {"status": "success"}
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Entry by specified foreign key/id doesn't exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
