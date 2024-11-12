from abc import ABC, abstractmethod
from typing import Generic, Type, Union, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_start.core.typing import T_MODEL


class BaseAbstractRepository(ABC, Generic[T_MODEL]):
    model: Type[T_MODEL]

    def __init__(self, session: AsyncSession):
        self.session = session


class AbstractCreate(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def create(self, data: dict) -> T_MODEL:
        raise NotImplementedError


class AbstractGet(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def get_by_id(self, id: Union[str, int, UUID]) -> Optional[T_MODEL]:
        raise NotImplementedError


class AbstractList(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def list(self, **kwargs) -> List[T_MODEL]:
        raise NotImplementedError


class AbstractDelete(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def delete(self, model: T_MODEL) -> None:
        raise NotImplementedError


class AbstractUpdate(BaseAbstractRepository[T_MODEL], ABC):
    @abstractmethod
    async def update(self, model: T_MODEL, data: dict) -> T_MODEL:
        raise NotImplementedError


class AbstractReadRepository(AbstractGet[T_MODEL], AbstractList[T_MODEL], ABC):
    pass


class AbstractWriteRepository(
    AbstractCreate[T_MODEL], AbstractUpdate[T_MODEL], AbstractDelete[T_MODEL], ABC
):
    pass


class AbstractRepository(
    AbstractWriteRepository[T_MODEL], AbstractReadRepository[T_MODEL], ABC
):
    pass
