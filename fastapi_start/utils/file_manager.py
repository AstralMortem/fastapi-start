from pathlib import Path
from pprint import pprint
from typing import Optional, Dict, Union, Type, List
import re


class File:
    def __init__(
        self, filename: str, content: str = "", replacer: Optional[dict] = None
    ):
        self.filename = self._check_filename(filename)
        self.content = content
        self.replacer = replacer

    @property
    def name(self):
        return self.filename

    def replace_content(self, with_save=False):
        pattern = r"\{\{\s*(\w+)\s*\}\}"
        if self.replacer is not None:
            content = re.sub(pattern, self.replace_keys, self.content)
            if with_save:
                self.content = content
            return content
        return self.content

    def replace_keys(self, match):
        key = match.group(1)
        return self.replacer.get(key, match.group(0))

    def update_replacer(self, d: Dict):
        self.replacer.update(d)

    def set_content(self, content):
        self.content = content

    def _check_filename(self, filename: str):
        if len(filename.rsplit(".", 1)) <= 1:
            raise ValueError("Filename must have at extension")
        return filename

    def __str__(self) -> str:
        return f"   {self.name}"

    def to_dict(self, parent_path: Union[str, Path] = "", create_root: bool = False):
        path = Path(parent_path, self.filename)
        self.replace_content(True)
        return {
            "name": self.name,
            "path": path,
            "content": self.content,
        }


class PyFile(File):
    def _check_filename(self, filename: str):
        try:
            filename = super()._check_filename(filename)
        except Exception:
            filename = f"{filename}.py"
        return filename


class Folder(list):
    def __init__(self, name: str, files: Optional[List[File]] = None):
        super().__init__()
        self._name = self._check_name(name)

        if files is not None:
            self.extend(files)

    @property
    def name(self):
        return self._name

    def append(self, item: Union[File, "Folder"]):
        if not isinstance(item, (File, Folder)):
            raise TypeError("Only File or Folder objects can be added")
        self._check_if_exists(item, File)
        self._check_if_exists(item, Folder)
        super().append(item)

    def extend(self, items: List[Union[File, "Folder"]]):
        for item in items:
            self.append(item)

    def _check_if_exists(self, item, obj: Union[Type[File], Type["Folder"]]):
        if isinstance(item, obj) and any(
            f.name == item.name for f in self if isinstance(f, obj)
        ):
            raise ValueError(
                f"{obj.__name__} with name '{item.name}' already exists in folder '{self.name}'."
            )

    def _check_name(self, name: str):
        if len(name.split(".")) > 1:
            raise ValueError(f"{name} must not have at extension")
        return name

    def __str__(self, level=0) -> str:
        indent = " " * (level * 2)
        result = f"{indent} {self.name}\n"
        for item in self:
            result += (
                f"{indent}{item}\n"
                if isinstance(item, File)
                else item.__str__(level + 1)
            )
        return result

    def to_dict(self, parent_path: Union[str, Path] = "", create_root=True):
        path = Path(parent_path).absolute()
        if create_root:
            path = path.joinpath(self.name)
        result = {"name": self.name, "path": str(path), "contents": []}
        for item in self:
            if isinstance(item, File):
                result["contents"].append(item.to_dict(path))
            elif isinstance(item, Folder):
                result["contents"].append(item.to_dict(path))
        return result


class PyModule(Folder):
    def __init__(self, name: str, files: Optional[List[File]] = None):
        super().__init__(name, files)
        self.append(File("__init__.py"))


class FileManager:

    @staticmethod
    def _check_is_empty(path: Path):
        if not Path(path).is_dir:
            raise ValueError("argument path should be a folder")
        if len(list(Path(path).iterdir())) > 0:
            raise RuntimeError(f"{path} folder is not empty")
        return True

    @staticmethod
    def _check_if_exists(path: Path):
        if not path.exists():
            raise RuntimeError(f"{path} folder is not exists")

    @staticmethod
    def _check_if_not_exists(path: Path):
        if path.exists():
            raise RuntimeError(f"{path} already exists")

    @staticmethod
    def pprint(root_folder):
        print("\n")
        print(root_folder)

    @staticmethod
    def build(structure: dict):
        Path(structure.get("path")).mkdir(exist_ok=True)
        for item in structure.get("contents", []):
            if "contents" in item:  # It's a folder
                folder_path = Path(item.get("path"))
                folder_path.mkdir(exist_ok=True)
                FileManager.build(item)
            else:  # It's a file
                file_path = Path(item.get("path"))
                with open(file_path, "w") as f:
                    f.write(item.get("content", ""))
                    f.close()

    @staticmethod
    def generate(root_folder, path: Optional[Union[str, Path]] = None):
        create_root = False
        if path is None:
            path = Path(".")
            create_root = True
            FileManager._check_if_not_exists(path.joinpath(root_folder.name))
        else:
            path = Path(path)
            FileManager._check_if_exists(path)
            FileManager._check_is_empty(path)
        structure = root_folder.to_dict(path, create_root)
        FileManager.build(structure)

    @staticmethod
    def insert(files: List[dict]):

        dummy = {"path": "", "contents": files}
        for file in files:
            FileManager._check_if_not_exists(Path(file.get("path")))
        FileManager.build(dummy)
