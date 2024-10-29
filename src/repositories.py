import math
from typing import Generic, TypeVar, Type

from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ItemNotFoundByIdException

T = TypeVar('T')
V = TypeVar('V')


class BaseRepo(Generic[T, V]):
    def __init__(self,
                 session: AsyncSession,
                 model: Type[T],
                 create_scheme: Type[V]):
        self.session = session
        self.model = model
        self.create_scheme = create_scheme

    async def create(self, scheme: V):
        create_smth = (
            insert(self.model)
            .values(**scheme.dict())
            .returning(self.model)
        )

        result = await self.session.execute(create_smth)
        await self.session.commit()
        return result.scalar_one()

    async def get_all(self, page: int, size: int):
        offset_min = page * size
        offset_max = (page + 1) * size

        select_smth = (
            select(self.model)
        )

        result = (await self.session.execute(select_smth)).scalars().all()
        response = result[offset_min:offset_max]

        return response

    async def get_by_id(self, id: int):
        select_smth = (
            select(self.model).filter_by(
                id=id
            )
        )

        result = (await self.session.execute(select_smth)).scalar_one_or_none()
        if not result:
            raise ItemNotFoundByIdException(f'Object with id {id} not found')
        return result

    async def delete_by_id(self, id: int):
        query = (
            select(self.model).filter_by(
                id=id
            )
        )

        result = (await self.session.execute(query)).scalar()
        if result:
            await self.session.delete(result)
            await self.session.commit()

    async def get_count(self):
        select_smth = (
            select(func.count(self.model.id))
        )

        result = (await self.session.execute(select_smth)).scalar()
        return result