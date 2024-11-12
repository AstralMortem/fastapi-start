from pathlib import Path

from dynaconf import inspect_settings

from fastapi_start.utils.file_manager import File, Folder, FileManager, PyModule, PyFile
from fastapi_start.utils.string import camel2snake, snake2camel

MANAGE_PY_CONTENT = """#!/usr/bin/env python
from pathlib import Path
import os

def main():
    BASE_DIR = Path(__file__).parent
    CONFIG_PATH = BASE_DIR.joinpath("core", "config.toml")
    os.environ.setdefault("FASTAPI_SETTINGS_MODULE", str(CONFIG_PATH))
    os.environ.setdefault("FASTAPI_BASE_DIR", f"@path {BASE_DIR}")
    try:
        from fastapi_start.core.cli import cli_app
    except ImportError as exc:
        raise ImportError('Could not import fastapi_start module, make sure you installed it.') from exc
    cli_app()
    
if __name__ == '__main__':
    main()
"""

ASGI_PY_CONTENT = """from fastapi_start.core.asgi import get_asgi
from pathlib import Path
import os
BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR.joinpath("core", "config.toml")
os.environ.setdefault("SETTINGS_MODULE", str(CONFIG_PATH))
os.environ.setdefault("BASE_DIR", f"@path {BASE_DIR}")
app = get_asgi()

"""

CONFIG_TOML_CONTENT = """# Main configuration file
DEBUG = true

ALEMBIC_MIGRATIONS_DIR = "@path {this.BASE_DIR}/models/migrations"
ALEMBIC_CONFIG_PATH = "@path {this.ALEMBIC_MIGRATIONS_DIR.parent}/alembic.ini"

DATABASE_URL = "@format sqlite+aiosqlite:///{this.BASE_DIR}/db.sqlite"
"""

ALEMBIC_INI_CONTENT = """
[alembic]
script_location = {{script_location}}

file_template = %%(slug)s-%%(rev)s_%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d

prepend_sys_path = .

truncate_slug_length = 40

version_locations = %(here)s/migrations

version_path_separator = os

output_encoding = utf-8

[post_write_hooks]
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

"""


def create_project(title, path):
    from fastapi_start.db import migrations

    root = Folder(title)

    core_folder = PyModule("core")
    asgi = File("asgi.py", ASGI_PY_CONTENT, {"project_name": title})
    config = File("config.toml", CONFIG_TOML_CONTENT)
    core_folder.extend([asgi, config])

    models_folder = PyModule("models")
    models_folder.append(Folder("migrations"))
    models_folder.append(
        File(
            "alembic.ini",
            ALEMBIC_INI_CONTENT,
            {"script_location": str(Path(migrations.__file__).parent.absolute())},
        )
    )

    services_folder = PyModule("services")

    entities_folder = PyModule("entities")

    routers_folder = PyModule("routes")

    repositories_folder = PyModule("repositories")

    manage = File("manage.py", MANAGE_PY_CONTENT, {"project_name": title})

    root.extend(
        [
            core_folder,
            models_folder,
            services_folder,
            entities_folder,
            routers_folder,
            repositories_folder,
            manage,
        ]
    )

    FileManager.generate(root, path)


def create_entity_file(name, fields):
    if fields:
        fields_str = "\n\t".join([f"{field[0]}: {field[1]}" for field in fields])
    else:
        fields_str = "pass"
    content = """from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, date


class {{entity_name}}DTO(BaseModel):
\t{{fields_str}}"""
    return PyFile(
        camel2snake(name),
        content,
        {"entity_name": snake2camel(name), "fields_str": fields_str},
    )


def create_model_file(name, fields):
    if fields:
        fields_str = "\n\t".join(
            [f"{field[0]}: Mapped[{field[1]}]" for field in fields]
        )
    else:
        fields_str = "pass"
    content = """from fastapi_start.db import models, Mapped, mapped_column
from uuid import UUID
from datetime import datetime, date


class {{model_name}}Model(models.Model):
\t{{fields_str}}"""
    return PyFile(
        camel2snake(name),
        content,
        {"model_name": snake2camel(name), "fields_str": fields_str},
    )


def create_service_file(name):
    from fastapi_start.conf import settings

    content = """from fastapi_start.services import CommonServiceImpl
from {{project_name}}.models.{{model_module}} import {{service_name}}Model

class {{service_name}}Service(CommonServiceImpl[{{service_name}}Model]):
    pass"""
    return PyFile(
        camel2snake(name),
        content,
        {
            "service_name": snake2camel(name),
            "project_name": settings.BASE_DIR.name,
            "model_module": camel2snake(name),
        },
    )


def create_repository_file(name):
    from fastapi_start.conf import settings

    content = """from abc import ABC, abstractmethod
from fastapi_start.repositories import CRUDRepositoryImpl, AbstractRepository
from {{project_name}}.models.{{model_module}} import {{repository_name}}Model


class {{repository_name}}AbstractRepository(AbstractRepository[{{repository_name}}Model], ABC):
    pass


class {{repository_name}}RepositoryImpl({{repository_name}}AbstractRepository, CRUDRepositoryImpl[{{repository_name}}Model]):
    pass"""
    return PyFile(
        camel2snake(name),
        content,
        {
            "repository_name": snake2camel(name),
            "project_name": settings.BASE_DIR.name,
            "model_module": camel2snake(name),
        },
    )


def create_entity(name, fields):
    from fastapi_start.conf import settings

    dto_file = create_entity_file(name, fields)
    model_file = create_model_file(name, fields)
    service_file = create_service_file(name)
    repository_file = create_repository_file(name)

    dto_file = dto_file.to_dict(settings.BASE_DIR.joinpath("entities"), False)
    model_file = model_file.to_dict(settings.BASE_DIR.joinpath("models"), False)
    service_file = service_file.to_dict(settings.BASE_DIR.joinpath("services"), False)
    repository_file = repository_file.to_dict(
        settings.BASE_DIR.joinpath("repositories"), False
    )

    FileManager.insert([dto_file, model_file, service_file, repository_file])
