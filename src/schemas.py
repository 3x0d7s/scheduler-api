import datetime
from typing import Optional, List, Generic, TypeVar

from pydantic import BaseModel

M = TypeVar('M')


class BaseScheme(BaseModel):
    # 'orm_mode' has been renamed to 'from_attributes'
    class Config:
        from_attributes = True


class TimedBaseScheme(BaseScheme):
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class PaginatedResponseScheme(BaseScheme, Generic[M]):
    result: Optional[List[M]]
    page: Optional[int] = 0
    totalPages: Optional[int] = 0
    size: Optional[int] = 10
    count: Optional[int] = 0
