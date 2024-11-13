from typing import TypeVar, Union
from uuid import UUID

from fastapi_start.db.models import Model
from fastapi_start.dto import DTO

T_MODEL = TypeVar("T_MODEL", bound=Model)

CREATE_DTO = TypeVar("CREATE_DTO", bound=DTO)
UPDATE_DTO = TypeVar("UPDATE_DTO", bound=DTO)
T_PK = TypeVar("T_PK", bound=Union[int, str, UUID])
