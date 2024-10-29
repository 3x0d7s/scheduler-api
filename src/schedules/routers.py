import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.events.repositories import EventsRepo
from src.events.schemas import EventRead
from src.exceptions import ItemNotFoundByIdException
from src.dependencies import get_pagination_params, PaginationParams
from src.responses import paginated_response_content
from src.schedules.repositories import ScheduleRepo
from src.schedules.schemas import ScheduleCreate, ScheduleWithOwnerRead, Schedule_Type
from src.schemas import PaginatedResponseScheme
from src.setup import get_async_session
from src.subscriptions.repositories import SubscriptionRepo
from src.subscriptions.schemas import SubscriberRead, SubscriptionCreate, Subscription_Type
from src.users.models import User

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
)

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginatedResponseScheme[ScheduleWithOwnerRead])
async def get_schedules(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user),
                        pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve schedules using this endpoint")

    repo = ScheduleRepo(session)

    count = await repo.get_count()
    result = await repo.get_all(page=pagination_params.page, size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/{id}", response_model=ScheduleWithOwnerRead)
async def get_schedule(id: int,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        repo = ScheduleRepo(session)

        result = await repo.get_by_id(id)

        if (result
                and not user.is_superuser
                and result.owner_id != user.id
                and result.schedule_type == Schedule_Type.PRIVATE):
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can retrieve schedules. You are none of them")

        return result
    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Schedule not found")


@router.get("/{id}/events", response_model=PaginatedResponseScheme[EventRead])
async def get_events_of_schedule(id: int, session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_user),
                                 pagination_params: PaginationParams = Depends(get_pagination_params)):
    try:
        schedule = await ScheduleRepo(session).get_by_id(id)

        if (schedule
                and not user.is_superuser
                and schedule.owner_id != user.id
                and schedule.schedule_type == Schedule_Type.PRIVATE):
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can retrieve schedules. You are none of them")

    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Schedule not found")

    repo = EventsRepo(session)

    events_count = await repo.get_events_count_by_schedule_id(schedule_id=id)
    events = await repo.get_all_by_schedule_id(schedule_id=id, 
                                               page=pagination_params.page, 
                                               size=pagination_params.size)

    return paginated_response_content(events, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      events_count)


@router.get("/{id}/subscribers", response_model=PaginatedResponseScheme[SubscriberRead])
async def get_subscribers_of_schedule(id: int, session: AsyncSession = Depends(get_async_session),
                                      user: User = Depends(current_user),
                                      pagination_params: PaginationParams = Depends(get_pagination_params)):
    try:
        schedule = await ScheduleRepo(session).get_by_id(id)

        if schedule and not user.is_superuser and schedule.owner_id != user.id:
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can see all schedules. You are none of them")
    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Schedule not found")

    repo = SubscriptionRepo(session)

    subscription_count = await repo.get_subscription_count_by_schedule_id(schedule_id=id)
    result = await repo.get_subscriptions_by_schedule_id(schedule_id=id, 
                                                          page=pagination_params.page, 
                                                          size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      subscription_count)


@router.post("/")
async def create_schedule(new_schedule: ScheduleCreate,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can create schedules using this endpoint")

    try:
        schedule_repo = ScheduleRepo(session)
        subscription_repo = SubscriptionRepo(session)

        created_schedule = await schedule_repo.create(new_schedule)

        new_subscription = SubscriptionCreate(
            subscriber_id=new_schedule.owner_id,
            schedule_id=created_schedule.id,
            subscription_type=Subscription_Type.OWNER
        )

        await subscription_repo.create(new_subscription)
        return {"status": "success"}
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Entry by specified foreign key/id doesn't exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}")
async def delete_schedule(id: int,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    repo = ScheduleRepo(session)
    try:
        schedule = await repo.get_by_id(id)

        if schedule and not user.is_superuser and schedule.owner_id != user.id:
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can see all schedules. You are none of them")
    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Schedule not found")

    await repo.delete_by_id(id)
    return {"status": "success"}
