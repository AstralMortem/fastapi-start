from fastapi_start.utils.file_manager import File, Folder, FileManager, PyModule

MANAGE_PY_CONTENT = """#!/usr/bin/env python
import os
def main():
    os.environ.setdefault("FASTAPI_SETTINGS", "{{project_name}}.config")
    try:
        from fastapi_start.core.cli import cli_app
    except ImportError as exc:
        raise ImportError('Could not import fastapi_start module, make sure you installed it.') from exc
    cli_app()
    
if __name__ == '__main__':
    main()
"""

ASGI_PY_CONTENT = """from fastapi_start.core.asgi import get_asgi
import os
os.environ.setdefault("FASTAPI_SETTINGS", "{{project_name}}.config")

app = get_asgi()

"""

CONFIG_TOML_CONTENT = """
DEBUG = true
"""


def create_project(title, path):
    root = Folder(title)
    manage = File("manage.py", MANAGE_PY_CONTENT, {"project_name": title})
    subroot = PyModule(title)
    asgi = File('asgi.py', ASGI_PY_CONTENT, {"project_name": title})
    config = File('config.toml', CONFIG_TOML_CONTENT)
    subroot.extend([asgi, config])
    root.extend([manage, subroot])

    FileManager.generate(root, path)

