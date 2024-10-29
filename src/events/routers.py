import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.dependencies import get_pagination_params, PaginationParams
from src.events.repositories import EventsRepo
from src.events.schemas import EventCreate, EventWithScheduleRead
from src.exceptions import ItemNotFoundByIdException
from src.responses import paginated_response_content
from src.schedules.repositories import ScheduleRepo
from src.schemas import PaginatedResponseScheme
from src.setup import get_async_session
from src.users.models import User


router = APIRouter(
    prefix="/events",
    tags=["events"],
)

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginatedResponseScheme[EventWithScheduleRead])
async def get_events(session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user),
                     pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can see all schedules using this endpoint")

    repo = EventsRepo(session)

    count = await repo.get_count()
    result = await repo.get_all(page=pagination_params.page, size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/{id}", response_model=EventWithScheduleRead)
async def get_event(id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    try:
        repo = EventsRepo(session)

        result = await repo.get_by_id(id)
        if result and (not user.is_superuser or result.schedule.owner_id != user.id):
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can see all schedules. You are none of them")

        return await repo.get_by_id(id)

    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Event not found")


@router.post("/")
async def create_event(new_event: EventCreate,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        repo = EventsRepo(session)

        # TODO: refactor this
        schedule = await ScheduleRepo(session).get_by_id(new_event.schedule_id)

        if not user.is_superuser and schedule.owner_id != user.id:
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule owner can see all schedules. You are none of them")

        await repo.create(new_event)
        return {"status": "success"}
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Entry by specified foreign key/id doesn't exists")


@router.delete("/{id}")
async def delete_event(id: int,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    # TODO: refactor this

    repo = EventsRepo(session)

    schedule = (await repo.get_by_id(id)).schedule

    if not user.is_superuser and schedule.owner_id != user.id:
        raise HTTPException(status_code=403,
                            detail="Only superusers or schedule owner can delete this schedule. You are none of them")

    await repo.delete_by_id(id)
    return {"status": "success"}
