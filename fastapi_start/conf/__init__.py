from dynaconf import Dynaconf, utils
from dynaconf.utils.parse_conf import BaseFormatter, Lazy

from . import global_settings
from pathlib import Path
import os

DEFAULT_SETTINGS = Path(global_settings.__file__)


def path_converter(path: str) -> Path:
    try:
        return Path(path).absolute()
    except Exception:
        raise ValueError(f"Invalid path: {path}")


utils.parse_conf.converters["@path"] = lambda value: Lazy(
    value,
    casting=path_converter,
)

settings = Dynaconf(
    load_dotenv=True,
    settings_files=[
        str(DEFAULT_SETTINGS),
        str(os.environ.get("FASTAPI_SETTINGS_MODULE")),
    ],
    merge_enabled=True,
    envvar_prefix="FASTAPI",
    environments=False,
)

__all__ = ["settings"]
