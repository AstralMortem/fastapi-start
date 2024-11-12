from typing import Union, Type, Optional, List
from uuid import UUID

from typing_extensions import Generic
from fastapi_start.dto import DTO
from fastapi_start.core.typing import T_MODEL
from fastapi_start.repositories.abstract import (
    BaseAbstractRepository,
    AbstractRepository,
    AbstractReadRepository,
    AbstractWriteRepository,
)


class BaseService(Generic[T_MODEL]):
    def __init__(
        self,
        repository: Union[
            BaseAbstractRepository[T_MODEL],
            AbstractRepository[T_MODEL],
            AbstractReadRepository[T_MODEL],
            AbstractWriteRepository[T_MODEL],
        ],
    ):
        self.repository = repository


class CommonServiceImpl(BaseService[T_MODEL]):
    async def _get_item(self, id: Union[int, str, UUID]) -> Optional[T_MODEL]:
        instance = await self.get_item(id)
        if not instance:
            raise ValueError("Item not found")
        return instance

    async def create_item(self, data: DTO) -> T_MODEL:
        validated_data = data.model_dump()
        return await self.repository.create(validated_data)

    async def get_item(self, id: Union[int, str, UUID]) -> Optional[T_MODEL]:
        instance = await self.repository.get_by_id(id)
        return instance

    async def list_items(self, **kwargs) -> List[T_MODEL]:
        return await self.repository.list(**kwargs)

    async def update_item(self, id: Union[int, str, UUID], data: DTO) -> T_MODEL:
        instance = await self._get_item(id)
        validated_data = data.model_dump()
        return await self.repository.update(instance, validated_data)

    async def patch_item(
        self, id: Union[int, str, UUID], data: DTO
    ) -> Optional[T_MODEL]:
        instance = await self._get_item(id)
        validated_data = data.model_dump(exclude_none=True, exclude_unset=True)
        return await self.repository.update(instance, validated_data)

    async def delete_item(self, id: Union[int, str, UUID]) -> None:
        instance = await self._get_item(id)
        await self.repository.delete(instance)
