from contextlib import asynccontextmanager, AsyncExitStack
from typing import Callable
from fastapi import FastAPI

SYS_LIFESPANS = []


def global_lifespan(user_lifespan=None):
    """
    set global lifespans before init app class
    """
    sys_lifespans = SYS_LIFESPANS

    if user_lifespan:
        if isinstance(user_lifespan, list):
            sys_lifespans.extend(user_lifespan)
        elif isinstance(user_lifespan, Callable):
            sys_lifespans.append(user_lifespan)
        else:
            raise Exception("You should pass @asyncontextmanager func or list of funcs")

    @asynccontextmanager
    async def _lifespan_manager(app: FastAPI):
        exit_stack = AsyncExitStack()
        async with exit_stack:
            for lifespan in sys_lifespans:
                await exit_stack.enter_async_context(lifespan(app))
            yield

    return _lifespan_manager