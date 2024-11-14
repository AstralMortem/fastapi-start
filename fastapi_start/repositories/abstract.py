from abc import ABC, abstractmethod
from typing import Generic, Type, Union, List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_start.core.typing import T_MODEL, T_PK
from fastapi_start.utils.pagination import PaginationParams, Page
from fastapi_start.utils.filter import Filter, FilterDepends


class BaseAbstractRepository(ABC, Generic[T_MODEL]):
    model: Type[T_MODEL]

    def __init__(self, session: AsyncSession):
        self.session = session


class AbstractCreate(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def create(self, data: dict) -> T_MODEL:
        raise NotImplementedError


class AbstractGet(Generic[T_PK, T_MODEL], BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def get_by_id(self, id: T_PK) -> Optional[T_MODEL]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, filters: Optional[Filter] = None) -> Optional[T_MODEL]:
        raise NotImplementedError


class AbstractList(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def list(
        self, pagination: PaginationParams, filters: Optional[Filter] = None
    ) -> Page[T_MODEL]:
        raise NotImplementedError


class AbstractDelete(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def delete(self, model: T_MODEL) -> None:
        raise NotImplementedError


class AbstractUpdate(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def update(self, model: T_MODEL, data: dict) -> T_MODEL:
        raise NotImplementedError


class AbstractReadRepository(
    Generic[T_PK, T_MODEL], AbstractGet[T_PK, T_MODEL], AbstractList[T_MODEL], ABC
):
    pass


class AbstractWriteRepository(
    AbstractCreate[T_MODEL], AbstractUpdate[T_MODEL], AbstractDelete[T_MODEL], ABC
):
    pass


class AbstractRepository(
    Generic[T_PK, T_MODEL],
    AbstractWriteRepository[T_MODEL],
    AbstractReadRepository[T_PK, T_MODEL],
    ABC,
):
    pass
