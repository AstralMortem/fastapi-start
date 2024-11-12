import os
from pathlib import Path
from pprint import pprint

import pytest
from dynaconf import inspect_settings


@pytest.fixture(scope="module", autouse=True)
def set_env_var():
    os.environ["SETTINGS_MODULE"] = str(Path("test_config.toml").absolute())
    yield
    del os.environ["SETTINGS_MODULE"]


@pytest.fixture
def settings(set_env_var):
    # import inside fixture to make sure that settings file loaded from env
    from fastapi_start.conf import settings as core_settings

    pprint(inspect_settings(core_settings))
    return core_settings


def test_init(settings):
    assert settings.DEBUG == True  # from test_config.toml
    assert settings.TITLE == "FastAPI start"  # from global_settings.py


def test_path_converter(settings):
    # Assuming you have a setting that uses @path
    settings.set("LOG_DIR", "@path /tmp/logs")  # Example, replace with actual setting
    log_dir = settings.LOG_DIR
    assert log_dir == Path("/tmp/logs").absolute()
    assert isinstance(log_dir, Path)
