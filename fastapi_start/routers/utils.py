from typing import Type, Union
from fastapi import APIRouter, status
from fastapi_start.routers.base import AbstractView


def path(endpoint: str, view: Union[Type[AbstractView], APIRouter], **router_kwargs):
    if isinstance(view, APIRouter):
        return view

    if issubclass(view, AbstractView):
        return view.as_view(endpoint, **router_kwargs)

    raise ValueError("Invalid view type. Expected View class or APIRouter instance.")
