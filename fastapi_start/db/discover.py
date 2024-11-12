from importlib import import_module
from .models import Model
import inspect


def discover_models(settings):
    models = []
    models_dir = settings.BASE_DIR.joinpath("models")
    for file in models_dir.iterdir():
        if file.is_file() and file.name.endswith(".py"):
            module = import_module(f"{settings.BASE_DIR.name}.models.{file.name[:-3]}")
            for name, member in inspect.getmembers(module, inspect.isclass):
                if issubclass(member, Model) and name != "Model":
                    models.append(member)
    return models
