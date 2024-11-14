from fastapi_start.core.management.file_managment import create_project


def test_project_creation():
    print(create_project("my_project"))
