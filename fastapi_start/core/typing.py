from typing import TypeVar
from fastapi_start.db.models import Model

T_MODEL = TypeVar("_MODEL", bound=Model)
