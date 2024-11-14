from abc import ABC, abstractmethod
from fastapi_start.repositories import CRUDRepositoryImpl, AbstractRepository
from ${project_name}.models.${snake_name} import ${camel_name}Model
% if len(fields) > 0 and fields[0][0] == "id" and fields[0][1] == "UUID":
from uuid import UUID
% endif


% if len(fields) > 0 and fields[0][0] == "id" and fields[0][1] == "UUID":

class Abstract${camel_name}Repository(AbstractRepository[UUID, ${camel_name}Model], ABC):
    pass

class ${camel_name}RepositoryImpl(Abstract${camel_name}Repository, CRUDRepositoryImpl[UUID, ${camel_name}Model]):
    model = ${camel_name}Model

% else:
class Abstract${camel_name}Repository(AbstractRepository[int, ${camel_name}Model], ABC):
    pass

class ${camel_name}RepositoryImpl(Abstract${camel_name}Repository, CRUDRepositoryImpl[int, ${camel_name}Model]):
    model = ${camel_name}Model
% endif
