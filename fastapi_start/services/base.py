from typing import Union, Type, Optional, List
from uuid import UUID

from typing_extensions import Generic
from fastapi_start.dto import DTO
from fastapi_start.core.typing import T_MODEL, T_PK
from fastapi_start.utils.filter import Filter
from fastapi_start.utils.pagination import PaginationParams, Page
from fastapi_start.repositories.abstract import (
    BaseAbstractRepository,
    AbstractRepository,
    AbstractReadRepository,
    AbstractWriteRepository,
)


class BaseService(Generic[T_PK, T_MODEL]):
    def __init__(
        self,
        repository: Union[
            BaseAbstractRepository[T_MODEL],
            AbstractRepository[T_PK, T_MODEL],
            AbstractReadRepository[T_PK, T_MODEL],
            AbstractWriteRepository[T_MODEL],
        ],
    ):
        self.repository = repository


class CommonServiceImpl(BaseService[T_PK, T_MODEL]):
    async def _get_item(self, id: T_PK) -> Optional[T_MODEL]:
        instance = await self.get_item(id)
        if not instance:
            raise ValueError("Item not found")
        return instance

    async def create_item(self, data: DTO) -> T_MODEL:
        validated_data = data.model_dump()
        return await self.repository.create(validated_data)

    async def get_item(self, id: T_PK) -> Optional[T_MODEL]:
        instance = await self.repository.get_by_id(id)
        return instance

    async def filter_item(self, filters: Optional[Filter] = None) -> Optional[T_MODEL]:
        return await self.repository.get(filters)

    async def list_items(
        self, pagination: PaginationParams, filters: Optional[Filter] = None
    ) -> Page[T_MODEL]:
        return await self.repository.list(pagination, filters)

    async def update_item(self, id: T_PK, data: DTO) -> T_MODEL:
        instance = await self._get_item(id)
        validated_data = data.model_dump()
        return await self.repository.update(instance, validated_data)

    async def patch_item(self, id: T_PK, data: DTO) -> Optional[T_MODEL]:
        instance = await self._get_item(id)
        validated_data = data.model_dump(exclude_none=True, exclude_unset=True)
        return await self.repository.update(instance, validated_data)

    async def delete_item(self, id: T_PK) -> None:
        instance = await self._get_item(id)
        await self.repository.delete(instance)
