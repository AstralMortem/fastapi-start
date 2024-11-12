import inspect

from fastapi import FastAPI
from fastapi_start.conf import settings
from .lifespan import global_lifespan
from importlib import import_module


class Application(FastAPI):
    def __init__(self, lifespan=None, **kwargs):
        super().__init__(
            debug=settings.DEBUG,
            title=settings.TITLE,
            description=settings.DESCRIPTION,
            version=settings.VERSION,
            lifespan=global_lifespan(lifespan),
            **kwargs,
        )
        self.init_router()

    def init_router(self):
        router_module = import_module(settings.BASE_ROUTER)
        endpoints = inspect.getmembers(router_module)
        for name, endpoints in endpoints:
            if name == "ENDPOINTS":
                for endpoint in endpoints:
                    print(endpoint)
                    self.include_router(endpoint)
                break


def get_asgi(lifespan=None, **kwargs):
    return Application(lifespan=lifespan, **kwargs)
