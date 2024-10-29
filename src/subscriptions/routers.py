import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import fastapi_users
from src.exceptions import ItemNotFoundByIdException
from src.dependencies import get_pagination_params, PaginationParams
from src.responses import paginated_response_content
from src.schemas import PaginatedResponseScheme
from src.setup import get_async_session
from src.subscriptions.repositories import SubscriptionRepo
from src.subscriptions.schemas import SubscriptionCreate, SubscriptionRead, Subscription_Type
from src.users.models import User

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)

current_user = fastapi_users.current_user()


@router.get("/", response_model=PaginatedResponseScheme[SubscriptionRead])
async def get_subscriptions(session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user),
                            pagination_params: PaginationParams = Depends(get_pagination_params)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve subscriptions using this endpoint")

    repo = SubscriptionRepo(session)

    count = await repo.get_count()
    result = await repo.get_all(page=pagination_params.page, size=pagination_params.size)

    return paginated_response_content(result, 
                                      pagination_params.page, 
                                      pagination_params.size, 
                                      count)


@router.get("/{id}", response_model=SubscriptionRead)
async def get_subscription(id: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    try:
        repo = SubscriptionRepo(session)

        result = await repo.get_by_id(id)

        if result and not user.is_superuser and result.subscriber_id != user.id:
            raise HTTPException(status_code=403,
                                detail="Only superusers or schedule subscriber can retrieve schedules. You are none "
                                       "of them")

        return result
    except ItemNotFoundByIdException:
        return []


@router.post("/")
async def create_subscription(new_schedule: SubscriptionCreate,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers can retrieve subscriptions using this endpoint")

    try:
        repo = SubscriptionRepo(session)

        await repo.create(new_schedule)
        return {"status": "success"}
    except IntegrityError:
        raise HTTPException(status_code=404, detail="Entry by specified foreign key/id doesn't exists")


@router.delete("/{id}")
async def delete_subscription(id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    repo = SubscriptionRepo(session)

    subscription = await repo.get_by_id(id)

    if not subscription:
        raise HTTPException(status_code=404, detail="Entry by specified id doesn't exists")

    if not user.is_superuser and subscription.subscriber_id != user.id:
        raise HTTPException(status_code=403,
                            detail="Only superusers or schedule follower can use this endpoint.You are none of them")

    await repo.delete_by_id(id)
    return {"status": "success"}
