import math

from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.dependencies import get_pagination_params, PaginationParams
from src.exceptions import ItemNotFoundByIdException
from src.responses import paginated_response_content
from src.schedules.repositories import ScheduleRepo
from src.schedules.schemas import ScheduleRead
from src.schemas import PaginatedResponseScheme
from src.setup import get_async_session
from src.subscriptions.repositories import SubscriptionRepo
from src.subscriptions.schemas import SubscriptionScheduleRead
from src.users.models import User
from src.users.repositories import UserRepo
from src.users.schemas import UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginatedResponseScheme[UserRead])
async def get_users(session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user),
                    pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve users using this endpoint")

    repo = UserRepo(session)

    count = await repo.get_count()
    result = await repo.get_all(page=pagination_params.page, size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/{id}", response_model=UserRead)
async def get_user(id: int,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    if not user.is_superuser and user.id != id:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve user info using this endpoint")

    try:
        repo = UserRepo(session)

        return await repo.get_by_id(id)
    except ItemNotFoundByIdException:
        raise HTTPException(status_code=404, detail="Schedule not found")


@router.get("/{id}/schedules", response_model=PaginatedResponseScheme[ScheduleRead])
async def get_owned_schedules(id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user),
                              pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser and user.id != id:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve user info using this endpoint")

    repo = ScheduleRepo(session)

    count = await repo.get_schedule_count_by_owner_id(owner_id=id)
    result = await repo.get_schedules_by_owner_id(owner_id=id, 
                                                  page=pagination_params.page, 
                                                  size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/{id}/subscriptions", response_model=PaginatedResponseScheme[SubscriptionScheduleRead])
async def get_subscriptions(id: int,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user),
                            pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser and user.id != id:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve subscriptions info using this endpoint")

    repo = SubscriptionRepo(session)

    count = await repo.get_subscription_count_by_owner_id(owner_id=id)
    result = await repo.get_subscriptions_by_subscriber_id(subscriber_id=id,
                                                          page=pagination_params.page,
                                                          size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.delete("/{id}")
async def delete_user(id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    if not user.is_superuser and user.id != id:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve subscriptions info using this endpoint")

    repo = UserRepo(session)

    await repo.delete_by_id(id)
    return {"status": "success"}
