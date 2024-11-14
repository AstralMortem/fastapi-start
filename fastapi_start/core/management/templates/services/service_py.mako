from fastapi_start.services import CommonServiceImpl
from ${project_name}.models.${snake_name} import ${camel_name}Model
from ${project_name}.repositories.${snake_name} import Abstract${camel_name}Repository
% if pk_field == "UUID":
from uuid import UUID
% endif



class ${camel_name}Service(CommonServiceImpl[${pk_field}, ${camel_name}Model]):
    def __init__(self, repository:Abstract${camel_name}Repository):
        super().__init__(repository)
