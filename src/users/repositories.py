from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User
from src.users.schemas import UserCreate
from src.repositories import BaseRepo


class UserRepo(BaseRepo[User, UserCreate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User, UserCreate)
