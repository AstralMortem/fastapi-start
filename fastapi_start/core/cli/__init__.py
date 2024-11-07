from typer import Typer
from .file_templates import create_project
cli_app = Typer()


@cli_app.command()
def startproject(title:str, path = None):
    create_project(title, path)


__all__ = ['cli_app']