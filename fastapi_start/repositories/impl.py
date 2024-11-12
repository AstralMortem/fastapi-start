from typing import Optional, Union, List, Any, Sequence
from uuid import UUID

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
from fastapi_start.core.typing import T_MODEL
from sqlalchemy import select, Row, RowMapping


class CreateRepositoryImpl(AbstractCreate[T_MODEL]):

    async def create(self, data: dict) -> T_MODEL:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


class GetRepositoryImpl(AbstractGet[T_MODEL]):
    async def get_by_id(self, id: Union[int, str, UUID]) -> Optional[T_MODEL]:
        instance = await self.session.get(self.model, id)
        return instance


class ListRepositoryImpl(AbstractList[T_MODEL]):
    async def list(self, **kwargs) -> Sequence[T_MODEL]:
        qs = select(self.model).filter_by(**kwargs)
        instances = await self.session.scalars(qs)
        return instances.all()


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
    AbstractReadRepository[T_MODEL],
    GetRepositoryImpl[T_MODEL],
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
    AbstractRepository[T_MODEL],
    ReadRepositoryImpl[T_MODEL],
    WriteRepositoryImpl[T_MODEL],
):
    pass
