from typing import (
    List,
    Callable,
    Type,
    Any,
    get_type_hints,
    Union,
    Generic,
    ClassVar,
    Optional,
)
from fastapi import APIRouter, Depends, Body
import inspect
from fastapi import Path
from pydantic.v1.typing import is_classvar
from starlette.responses import JSONResponse
from .base import AbstractView, Metadata, RouteType, HTTPMethod
from fastapi_start.services import CommonServiceImpl
from fastapi_start.dto import DTO
from fastapi_start.core.typing import CREATE_DTO, UPDATE_DTO, T_PK
from fastapi_start.utils.filter import Filter, FilterDepends
from fastapi_start.utils.pagination import PaginationParams

METADATA_VAR = "__metadata__"
CBV_VAR = "__cbv_class__"
INCLUDE_INIT_PARAMS_KEY = "__include_init_params__"
RETURN_TYPES_FUNC_KEY = "__return_types_func__"


class GenericView(AbstractView):
    ACTIONS_MAP = {
        "list": HTTPMethod.GET,
        "get": HTTPMethod.GET,
        "post": HTTPMethod.POST,
        "update": HTTPMethod.PUT,
        "delete": HTTPMethod.DELETE,
        "patch": HTTPMethod.PATCH,
    }

    @classmethod
    def as_view(cls, endpoint: str = "/", **router_kwargs):
        router = APIRouter(prefix=endpoint, **router_kwargs)
        cls._init_cbv()
        obj = cls

        for _callable_name, _callable in inspect.getmembers(obj, inspect.isfunction):
            if _callable_name in obj.ACTIONS_MAP or hasattr(_callable, METADATA_VAR):
                metadata: Metadata = getattr(
                    _callable,
                    METADATA_VAR,
                    Metadata(methods=[obj.ACTIONS_MAP.get(_callable_name)]),
                )
                # TODO: Add exceptions
                _path = "/"
                if metadata and metadata.path:
                    _path += metadata.path

                metadata.type = metadata.type
                metadata.path = _path
                metadata.methods = list(metadata.methods)
                metadata.response_class = (
                    metadata.response_class
                    or obj.RESPONSE_CLASSES.get(_callable_name, JSONResponse)
                )
                metadata.response_model = (
                    metadata.response_model or obj.RESPONSE_MODELS.get(_callable_name)
                )
                metadata.name = metadata.name or cls.name_parser(cls, _callable_name)
                metadata.status_code = metadata.status_code or obj.default_status_code

                cls._register_route(_callable, metadata, router)
        return router

    @classmethod
    def _register_route(cls, callable: Callable, metadata: Metadata, router: APIRouter):
        meta = metadata.model_dump(exclude_none=True, exclude_unset=True)
        path_url = cls._update_cbv_route_endpoint_signature(callable)
        if path_url:
            meta["path"] = meta["path"] + path_url
        route_type = meta.pop("type")
        if route_type == RouteType.ROUTE:
            router.add_api_route(endpoint=callable, **meta)
        elif route_type == RouteType.WEBSOCKET:
            router.add_websocket_route(endpoint=callable, **meta)
        else:
            router.add_route(endpoint=callable, **meta)

    @classmethod
    def _update_cbv_route_endpoint_signature(
        cls: Type[Any], endpoint: Callable
    ) -> None:
        """
        Fixes the endpoint signature for a cbv route to ensure FastAPI performs dependency injection properly.
        """
        old_endpoint = endpoint
        old_signature = inspect.signature(old_endpoint)
        old_parameters: List[inspect.Parameter] = list(
            old_signature.parameters.values()
        )
        old_first_parameter = old_parameters[0]
        new_first_parameter = old_first_parameter.replace(default=Depends(cls))
        new_parameters = [new_first_parameter] + [
            parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
            for parameter in old_parameters[1:]
        ]

        new_signature = old_signature.replace(parameters=new_parameters)
        setattr(endpoint, "__signature__", new_signature)
        for i in new_parameters:
            if i.name != "self":
                if type(i.default).__name__ == Path.__name__:
                    return "{" + i.name + "}"

    @classmethod
    def _init_cbv(cls, instance: Any = None) -> None:
        if getattr(cls, CBV_VAR, False):  # pragma: no cover
            return  # Already initialized
        old_init: Callable[..., Any] = cls.__init__
        old_signature = inspect.signature(old_init)
        old_parameters = list(old_signature.parameters.values())[
            1:
        ]  # drop `self` parameter
        new_parameters = [
            x
            for x in old_parameters
            if x.kind
            not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        ]

        dependency_names: List[str] = []
        for name, hint in get_type_hints(cls).items():
            if is_classvar(hint):
                continue
            parameter_kwargs = {"default": getattr(cls, name, Ellipsis)}
            dependency_names.append(name)
            new_parameters.append(
                inspect.Parameter(
                    name=name,
                    kind=inspect.Parameter.KEYWORD_ONLY,
                    annotation=hint,
                    **parameter_kwargs
                )
            )
        new_signature = inspect.Signature(())
        if not instance or hasattr(cls, INCLUDE_INIT_PARAMS_KEY):
            new_signature = old_signature.replace(parameters=new_parameters)

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            for dep_name in dependency_names:
                dep_value = kwargs.pop(dep_name)
                setattr(self, dep_name, dep_value)
            if instance and not hasattr(cls, INCLUDE_INIT_PARAMS_KEY):
                self.__class__ = instance.__class__
                self.__dict__ = instance.__dict__
            else:
                old_init(self, *args, **kwargs)

        setattr(cls, "__signature__", new_signature)
        setattr(cls, "__init__", new_init)
        setattr(cls, CBV_VAR, True)


class DefaultView(Generic[T_PK, CREATE_DTO, UPDATE_DTO], GenericView):
    service: CommonServiceImpl

    create_dto: ClassVar[CREATE_DTO]
    update_dto: ClassVar[UPDATE_DTO]
    pk_field: ClassVar[T_PK]

    async def list(
        self,
        pagination: PaginationParams = Depends(),
        filters: Optional[Type[Filter]] = FilterDepends(Filter),
    ):
        return await self.service.list_items(pagination, filters)

    async def get(self, id: T_PK = Path()):
        return await self.service.get_item(id)

    async def post(self, data: CREATE_DTO):
        return await self.service.create_item(data)

    async def patch(self, data: UPDATE_DTO, id: T_PK = Path()):
        return await self.service.patch_item(id, data)

    async def delete(self, id: T_PK = Path()):
        return await self.service.delete_item(id)

    @classmethod
    def as_view(cls, *args, **kwargs):
        router = super().as_view(*args, **kwargs)
        cls._init_dto(router)
        return router

    @classmethod
    def _init_dto(cls, router):
        for route in router.routes:
            old_endpoint = route.endpoint
            old_signature = inspect.signature(old_endpoint)
            old_parameters: List[inspect.Parameter] = list(
                old_signature.parameters.values()
            )

            new_parameters = []
            for param in old_parameters:
                if param.name != "data" and param.name != "id":
                    local_param = param
                else:
                    if param.name == "data":
                        if route.endpoint.__name__ == "post":
                            local_param = param.replace(annotation=cls.create_dto)
                        else:
                            local_param = param.replace(annotation=cls.update_dto)
                    elif param.name == "id":
                        local_param = param.replace(annotation=cls.pk_field)
                    else:
                        continue
                new_parameters.append(local_param)
            new_signature = old_signature.replace(parameters=new_parameters)
            setattr(route.endpoint, "__signature__", new_signature)
