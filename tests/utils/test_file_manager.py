from pathlib import Path

from fastapi_start.utils.file_manager import File, Folder, FileManager
from pytest import raises, fixture

@fixture
def get_file():
    return File('test.py', 'test content {{key1}}', {'key1': 'value1'})

@fixture
def get_structure():
    test_str = 'this is {{key1}} str {{key2}}'
    test_dict = {'key1': 'value1', 'key2': 'value2'}
    root = Folder('root')
    sub = Folder('sub')
    sub.append(File('file1.py', test_str, test_dict))
    sub.append(File('file2.py', test_str, test_dict))
    sub.append(File('file3.py', test_str, test_dict))
    root.append(File('file4.py', test_str, test_dict))
    root.append(sub)
    return root

def test_file_init(get_file):
    file = File('test.py')
    assert file.filename == 'test.py'
    assert file.name ==  'test.py'

    with raises(ValueError):
        File('test')

    file3 = get_file
    assert file3.filename == 'test.py'
    assert file3.content == 'test content {{key1}}'

def test_file_replacer(get_file):
    test_dict = {'key1': 'value1'}
    test_str = 'test content {{key1}}'
    res_str = test_str.replace("{{key1}}", test_dict['key1'])

    file = get_file
    file.replace_content(True)
    assert file.content == res_str



def test_folder_init(get_file):
    folder = Folder('test')
    assert folder.name == 'test'

    with raises(ValueError):
        Folder('test.py')


def test_folder_append(get_file):
    folder = Folder('test')
    folder2 = Folder('test2', [get_file])

    folder.append(get_file)
    folder.append(folder2)

    assert folder == [get_file, folder2]
    with raises(ValueError):
        folder.append(get_file)

    with raises(ValueError):
        folder.append(folder2)

    with raises(TypeError):
        folder.append(10)


def test_file_manager_init(get_structure):
    test_folder = Path('.', 'test_folder')
    test_folder.mkdir(exist_ok=True)

    root_folder = get_structure
    with raises(RuntimeError):
        FileManager.generate(root_folder, ".")

    FileManager.generate(root_folder)
    FileManager.generate(root_folder, 'test_folder')
    with raises(RuntimeError):
        FileManager.generate(root_folder, 'test_folder')

    import shutil
    shutil.rmtree(test_folder)
    shutil.rmtree(Path('.', root_folder.name))