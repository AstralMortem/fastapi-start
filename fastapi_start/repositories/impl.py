from typing import Optional
from .abstract import (
    AbstractUpdate,
    AbstractGet,
    AbstractList,
    AbstractRepository,
    AbstractReadRepository,
    AbstractWriteRepository,
    AbstractCreate,
    AbstractDelete,
)
from fastapi_start.core.typing import T_MODEL, T_PK
from fastapi_start.utils.filter import Filter
from fastapi_start.utils.pagination import PaginationParams, Page, paginate
from sqlalchemy import select


class CreateRepositoryImpl(AbstractCreate[T_MODEL]):

    async def create(self, data: dict) -> T_MODEL:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


class GetRepositoryImpl(AbstractGet[T_PK, T_MODEL]):
    async def get_by_id(self, id: T_PK) -> Optional[T_MODEL]:
        instance = await self.session.get(self.model, id)
        return instance

    async def get(self, filters: Optional[Filter] = None) -> Optional[T_MODEL]:
        qs = select(self.model)
        if filters:
            qs = filters.filter(qs)
        return await self.session.scalar(qs)


class ListRepositoryImpl(AbstractList[T_MODEL]):
    async def list(
        self, pagination: PaginationParams, filters: Optional[Filter] = None
    ) -> Page[T_MODEL]:
        qs = select(self.model)
        if filters:
            qs = filters.filter(qs)

        return await paginate(self.session, qs, pagination)


class DeleteRepositoryImpl(AbstractDelete[T_MODEL]):
    async def delete(self, model: T_MODEL) -> None:
        await self.session.delete(model)


class UpdateRepositoryImpl(AbstractUpdate[T_MODEL]):
    async def update(self, model: T_MODEL, data: dict) -> T_MODEL:
        for key, value in data.items():
            setattr(model, key, value)
        await self.session.commit()
        await self.session.refresh(model)
        return model


class ReadRepositoryImpl(
    AbstractReadRepository[T_PK, T_MODEL],
    GetRepositoryImpl[T_PK, T_MODEL],
    ListRepositoryImpl[T_MODEL],
):
    pass


class WriteRepositoryImpl(
    AbstractWriteRepository[T_MODEL],
    CreateRepositoryImpl[T_MODEL],
    UpdateRepositoryImpl[T_MODEL],
    DeleteRepositoryImpl[T_MODEL],
):
    pass


class CRUDRepositoryImpl(
    AbstractRepository[T_PK, T_MODEL],
    ReadRepositoryImpl[T_PK, T_MODEL],
    WriteRepositoryImpl[T_MODEL],
):
    pass
