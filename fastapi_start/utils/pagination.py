from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import add_pagination, Page, Params as PaginationParams


@asynccontextmanager
async def init_pagination(app: FastAPI):
    add_pagination(app)
    yield


__all__ = ["paginate", "Page", "PaginationParams", "init_pagination"]
