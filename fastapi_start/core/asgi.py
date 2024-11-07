from fastapi import FastAPI
from fastapi_start.conf import settings
from .lifespan import global_lifespan

class Application(FastAPI):
    def __init__(self, lifespan = None, **kwargs):
        super().__init__(
            debug=settings.DEBUG,
            title=settings.TITLE,
            description=settings.DESCRIPTION,
            version=settings.VERSION,
            lifespan=global_lifespan(lifespan)
            **kwargs
        )


def get_asgi(lifespan = None, **kwargs):
    return Application(lifespan=lifespan, **kwargs)