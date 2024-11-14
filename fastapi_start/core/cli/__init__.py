import uvicorn
import typer
from rich import print
from fastapi_start.core.management.file_managment import create_project, create_entity
from alembic.config import Config as AlembicConfig
from alembic import command as alembic_command

cli_app = typer.Typer()


@cli_app.command()
def startproject(title: str, path=""):
    try:
        create_project(title, path)
        print(f"[green]Project {title} created successfully.[/green]")
    except Exception as e:
        print(f"[red]Error creating project: [bold]{e}[/bold][/red]")


@cli_app.command()
def createentity():
    name = typer.prompt("Enter the name of the entity")
    interactive = typer.confirm("Do you want to add fields to the entity?")
    fields = []
    if interactive:
        while True:
            field = typer.prompt(
                "Enter field name and type (e.g., name:str, age:int) or 'q' to finish"
            )
            if field.lower() == "q":
                break
            fields.append(field.rsplit(":", 1))
    try:
        create_entity(name, fields)
        print(f"[green]Entity {name} created successfully.[/green]")
    except Exception as e:
        print(f"[red]Error creating entity: {e}[/red]")


@cli_app.command()
def runserver(
    host: str = None,
    port: int = None,
    settings: str = None,
    reloads: bool = True,
):
    local_host = host or "127.0.0.1"
    local_port = port or 8000
    if ":" in local_host:
        local_host, local_port = host.split(":")

    from fastapi_start.conf import settings

    uvicorn.run(
        "core.asgi:app",
        host=local_host,
        port=local_port,
        reload=reloads,
        reload_dirs=[settings.BASE_DIR],
    )


@cli_app.command()
def makemigrations(message: str = "init", autogenerate: bool = True):
    from fastapi_start.conf import settings

    config = AlembicConfig(settings.ALEMBIC_CONFIG_PATH)
    alembic_command.revision(
        config,
        message=message,
        autogenerate=autogenerate,
        version_path=str(settings.ALEMBIC_MIGRATIONS_DIR),
    )


@cli_app.command()
def migrate(revision: str = "head", sql: bool = False):
    from fastapi_start.conf import settings

    config = AlembicConfig(settings.ALEMBIC_CONFIG_PATH)
    # config.set_main_option("script_location", str(settings.ALEMBIC_CONFIG_PATH.parent))
    alembic_command.upgrade(config, revision, sql=sql)


@cli_app.command()
def downgrade(revision: str, sql: bool = False):
    from fastapi_start.conf import settings

    config = AlembicConfig(settings.ALEMBIC_CONFIG_PATH)
    alembic_command.downgrade(config, revision, sql=sql)


__all__ = ["cli_app"]
