from typing import Optional

from fastapi_users import schemas, models
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str

    id: models.ID
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str

    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
