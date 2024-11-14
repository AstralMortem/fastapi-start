from pathlib import Path
from typing import List

from .file import File, Folder, templates_lookup
from fastapi_start.db import migrations
from fastapi_start.utils.string import camel2snake, snake2camel


def get_file(file_path: str, **context):
    template_name = file_path.replace(".", "_") + ".mako"
    file_name = file_path.rsplit("/")[-1]

    return File(file_name, template_name, context)


def create_project(project_name: str, path: str = ""):
    root = Folder(project_name)
    root.append(get_file("manage.py"))
    root.append(get_file("core/dependencies.py"))

    core_folder = Folder("core")
    core_folder.append(File("__init__.py"))
    core_folder.append(get_file("core/asgi.py"))
    core_folder.append(get_file("core/config.toml"))

    models_folder = Folder("models")
    models_folder.append(File("__init__.py"))
    models_folder.append(
        get_file(
            "models/alembic.ini",
            script_location=str(Path(migrations.__file__).parent.absolute()),
        )
    )
    models_folder.append(Folder("migrations"))

    services_folder = Folder("services")
    services_folder.append(File("__init__.py"))

    entities_folder = Folder("entities")
    entities_folder.append(File("__init__.py"))

    repositories_folder = Folder("repositories")
    repositories_folder.append(File("__init__.py"))

    routers_folder = Folder("routes")
    routers_folder.append(get_file("routes/__init__.py"))

    root.extend(
        [
            core_folder,
            models_folder,
            services_folder,
            entities_folder,
            routers_folder,
            repositories_folder,
        ]
    )

    root.create(path)


def add_entity_to_root(
    root: Folder, subroot_name: str, file_name: str, template_name: str, **context
):
    file = File(file_name, template_name, context)
    folder = Folder(subroot_name)
    folder.append(file)
    root.append(folder)


def override_dependencies(global_context):
    from fastapi_start.conf import settings

    dependencies_path = settings.BASE_DIR.joinpath("dependencies.py")
    lines = open(dependencies_path, "r").readlines()
    old_imports = []
    old_code = []

    for line in lines:
        if line.startswith("from") or line.startswith("import"):
            old_imports.append(line)
        else:
            old_code.append(line)

    context = {"old_imports": old_imports, "old_code": old_code}
    context.update(global_context)

    content = templates_lookup.get_template("core/newdependencies_py.mako").render(
        **context
    )
    open(dependencies_path, "w").write(content)


def override_main_router(global_context):
    from fastapi_start.conf import settings

    routers_path = settings.BASE_DIR.joinpath("routes/__init__.py")
    lines = open(routers_path, "r").readlines()
    old_imports = []
    old_code = []
    old_paths = []

    for line in lines:
        if line.startswith("from") or line.startswith("import"):
            old_imports.append(line)
        else:
            old_code.append(line)

    for code in old_code:
        if code.strip().startswith("ENDPOINTS") or (
            code.strip().endswith("]") or code.strip().startswith("]")
        ):
            continue
        old_paths.append(code.strip())
    print(old_code)
    print(old_paths)

    context = {"old_imports": old_imports, "old_code": old_paths}
    context.update(global_context)

    content = templates_lookup.get_template("routes/newinit_py.mako").render(**context)

    open(routers_path, "w").write(content)


def create_entity(entity_name: str, fields: List[str]):
    from fastapi_start.conf import settings

    project_name = settings.BASE_DIR.name
    entity_name = camel2snake(entity_name)
    entity_name_camel = snake2camel(entity_name)
    entity_file_name = f"{entity_name}.py"

    root = Folder(project_name)
    global_context = {
        "project_name": project_name,
        "snake_name": entity_name,
        "camel_name": entity_name_camel,
        "fields": fields,
        "pk_field": fields[0][1] if len(fields) > 0 and fields[0][0] == "id" else "_",
    }

    inserts = [
        ("models", "models/model_py.mako", entity_file_name, {}),
        ("services", "services/service_py.mako", entity_file_name, {}),
        ("entities", "entities/entity_py.mako", entity_file_name, {}),
        ("repositories", "repositories/repository_py.mako", entity_file_name, {}),
        ("routes", "routes/route_py.mako", entity_file_name, {}),
    ]

    for subroot, template_name, file_name, context in inserts:
        context.update(global_context)
        add_entity_to_root(root, subroot, file_name, template_name, **context)

    root.insert(settings.BASE_DIR)

    override_dependencies(global_context)
    override_main_router(global_context)
