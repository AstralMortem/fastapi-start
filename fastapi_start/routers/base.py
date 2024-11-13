import logging
import re
from abc import abstractmethod, ABC
from enum import Enum
from functools import wraps
from typing import Iterable, Type, List, Callable
from fastapi import Response, HTTPException, status
from pydantic import BaseModel
from fastapi_start.dto import DTO

logger = logging.getLogger("fastapi_class")


def _view_class_name_default_parser(cls: object, method: str):
    class_name = " ".join(re.findall(r"[A-Z][^A-Z]*", cls.__name__.replace("View", "")))  # type: ignore
    return f"{method.capitalize()} {class_name}"


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    PUT = "put"


class RouteType(str, Enum):
    ROUTE = "route"
    WEBSOCKET = "websocket"


class Metadata(BaseModel):
    methods: List[str | HTTPMethod]
    type: RouteType = RouteType.ROUTE
    name: str | None = None
    path: str | None = None
    status_code: int | None = None
    response_model: Type[DTO] | None = None
    response_class: Type[Response] | None = None
    exceptions: Iterable[Type[HTTPException]] | None = None


class AbstractView(ABC):
    RESPONSE_MODELS = {}
    RESPONSE_CLASSES = {}
    EXCEPTIONS = {}
    ACTIONS_MAP = {}

    name_parser = _view_class_name_default_parser
    default_status_code = status.HTTP_200_OK

    @classmethod
    @abstractmethod
    def as_view(cls, path: str, **router_kwargs):
        raise NotImplementedError


def endpoint(
    methods: Iterable[str | HTTPMethod] | str | None = None,
    *,
    name: str | None = None,
    path: str | None = None,
    status_code: int | None = None,
    response_model: type[DTO] | None = None,
    response_class: type[Response] | None = None,
):

    assert all(
        issubclass(_type, expected_type)
        for _type, expected_type in (
            (response_model, DTO),
            (response_class, Response),
        )
        if _type is not None
    ), "Response model and response class must be subclasses of BaseModel and Response respectively."
    assert (
        isinstance(methods, (Iterable, str)) or methods is None
    ), "Methods must be an string, iterable of strings or Method enums."

    def _decorator(function: Callable):
        """
        Decorate the function.
        """

        @wraps(function)
        async def _wrapper(*args, **kwargs):
            """
            Wrapper for the function.
            """
            return await function(*args, **kwargs)

        parsed_method = set()
        _methods = (
            (methods,)
            if isinstance(methods, str)
            else methods or ((name,) if name else (function.__name__,))
        )
        for method in _methods:
            if isinstance(method, HTTPMethod):
                parsed_method.add(method)
                continue
            try:
                parsed_method.add(HTTPMethod[method.upper()])
            except KeyError as exc:
                raise ValueError(f"HTTP Method {method} is not allowed") from exc
        _wrapper.__metadata__ = Metadata(  # type: ignore
            methods=parsed_method,
            name=name,
            path=path,
            status_code=status_code,
            response_class=response_class,
            response_model=response_model,
        )
        return _wrapper

    return _decorator
