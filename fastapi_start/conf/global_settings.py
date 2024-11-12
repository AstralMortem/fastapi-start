from importlib import import_module
from inspect import getfile
from pathlib import Path
from fastapi_start import db

DEBUG: bool = False
TITLE: str = "FastAPI start"
DESCRIPTION: str = "FastAPI start"
VERSION: str = "0.1.0"


DB_SESSION_PARAMS = {"echo": True}
