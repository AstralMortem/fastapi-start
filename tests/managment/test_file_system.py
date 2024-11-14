from fastapi_start.core.management.file import File, Folder
from pathlib import Path

import pytest


@pytest.fixture
def get_template():
    from fastapi_start.core import management

    TEMPLATE_NAME = "manage_py.mako"
    content = open(
        Path(management.__file__).parent.joinpath("templates").joinpath(TEMPLATE_NAME),
        "r",
    ).read()
    return TEMPLATE_NAME, content


@pytest.fixture
def folder_init():
    import shutil

    folder = Path("test_project")
    if folder.exists():
        yield folder
    else:
        folder = Path("test_folder")
        yield folder

    shutil.rmtree(folder)


def test_file(get_template):
    temp_name, temp_content = get_template

    file = File("manage.py", temp_name)
    assert file.name == "manage.py"
    assert file.template_content.render() == temp_content


def test_folder(get_template):
    temp_name, temp_content = get_template

    file = File("manage.py", temp_name)

    folder = Folder("test_folder")
    folder.name == "test_folder"

    folder.append(file)
    folder.children[0] == file
    with pytest.raises(Exception):
        folder.append(file)


def test_stucture(get_template, folder_init):
    temp_name, temp_content = get_template
    file = File("manage.py", temp_name)

    folder = Folder("test_folder")
    folder.append(file)

    with pytest.raises(Exception):
        folder.create(".")
    folder.create("")

    test_folder_path = folder_init

    assert open(test_folder_path.joinpath("manage.py"), "r").read() == temp_content
