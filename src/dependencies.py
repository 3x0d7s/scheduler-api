from fastapi import Query
from pydantic import BaseModel
from fastapi import Depends

class PaginationParams(BaseModel):
    page: int = Query(ge=0, default=0)
    size: int = Query(ge=1, le=100, default=10)


async def get_pagination_params(pagination_params: PaginationParams = Depends()):
    return pagination_params
