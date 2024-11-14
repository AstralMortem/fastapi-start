from fastapi_start.dto import DTO
from datetime import datetime, date
from fastapi_start.utils.filter import Filter
from ${project_name}.models.${snake_name} import ${camel_name}Model
% if len(fields) > 0 and fields[0][0] == "id" and fields[0][1] == "UUID":
from uuid import UUID
% endif


class ${camel_name}DTO(DTO):
% if len(fields) == 0:
    pass
% else:
% for field_name, field_type in fields:
    ${field_name}: ${field_type}
% endfor
% endif

class ${camel_name}CreateDTO(DTO):
% if len(fields) == 0:
    pass
% else:
% for field_name, field_type in fields:
% if field_name == "id":
<% continue %>
% else:
    ${field_name}: ${field_type}
% endif
% endfor
% endif

class ${camel_name}UpdateDTO(DTO):
% if len(fields) == 0:
    pass
% else:
% for field_name, field_type in fields:
% if field_name == "id":
<% continue %>
% else:
    ${field_name}: ${field_type} | None = None
% endif
% endfor
% endif

class ${camel_name}Filter(${camel_name}UpdateDTO, Filter):
    class Constants(Filter.Constants):
        model = ${camel_name}Model
