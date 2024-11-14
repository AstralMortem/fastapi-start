from fastapi_start.db import models, Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, date


class ${camel_name}Model(models.Model):
% if len(fields) == 0:
    pass
%else:
% for field_name, field_type in fields:

    % if field_name == 'id':
    % if field_type == 'UUID':
    ${field_name}: Mapped[${field_type}] = mapped_column(primary_key=True, default=uuid4)
    %else:
    ${field_name}: Mapped[${field_type}] = mapped_column(primary_key=True)
    %endif
    % else:
    ${field_name}: Mapped[${field_type}]
    % endif

% endfor
% endif