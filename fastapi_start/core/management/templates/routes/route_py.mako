from fastapi import Depends, Path
from fastapi_start.routers import GenericView, endpoint
from fastapi_start.utils.pagination import PaginationParams, Page
from fastapi_start.utils.filter import FilterDepends
from ${project_name}.entities.${snake_name} import ${camel_name}DTO, ${camel_name}CreateDTO, ${camel_name}UpdateDTO, ${camel_name}Filter
from ${project_name}.services.${snake_name} import ${camel_name}Service
from ${project_name}.dependencies import get_${snake_name}_service
% if pk_field == "UUID":
from uuid import UUID
%endif


class ${camel_name}View(GenericView):
    pk_field = int
    create_dto = ${camel_name}CreateDTO
    update_dto = ${camel_name}UpdateDTO
    service: ${camel_name}Service = Depends(get_${snake_name}_service)

    RESPONSE_MODELS = {
        "get": ${camel_name}DTO,
        "post": ${camel_name}DTO,
        "patch": ${camel_name}DTO,
        "list": Page[${camel_name}DTO],
    }

    async def get(self, id: ${pk_field} = Path()):
        return await self.service.get_item(id)

    async def list(self, pagination: PaginationParams = Depends(), filters: ${camel_name}Filter = FilterDepends(${camel_name}Filter)):
        return await self.service.list_items(pagination, filters)

    async def post(self, data: ${camel_name}CreateDTO):
        return await self.service.create_item(data)

    async def patch(self,data: ${camel_name}UpdateDTO, id: ${pk_field} = Path()):
        return await self.service.patch_item(id, data)

    async def delete(self, id: ${pk_field} = Path()):
        return await self.service.delete_item(id)