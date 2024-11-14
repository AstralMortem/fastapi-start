from typing import Optional, List, Union
from mako.lookup import TemplateLookup
from pathlib import Path
from mako.template import Template


TEMPLATES_FOLDER = Path(__file__).parent.joinpath("templates")
templates_lookup = TemplateLookup(
    TEMPLATES_FOLDER, module_directory="/tmp/mako_modules"
)


class File:
    def __init__(
        self, name: str, template_name: Optional[str] = None, context: dict = None
    ):
        self.name = name
        self.template_content = (
            templates_lookup.get_template(template_name)
            if template_name
            else Template("")
        )
        self.context = context

    def _render_content(self):
        if self.context is not None:
            return self.template_content.render(**self.context)
        return self.template_content.render()

    def set_context(self, **kwargs):
        self.context = kwargs

    def set_content(self, content: str, direct_text: bool = False):
        if direct_text:
            self.template_content = Template(content)
        else:
            self.template_content = templates_lookup.get_template(content)

    def create(self, path: Union[str, Path]):
        full_path = Path(path, self.name)
        if not full_path.exists():
            content = self._render_content()

            with open(full_path, "w") as f:
                f.write(content)
        else:
            raise Exception(f"File {self.name} in {full_path} already exists.")


class Folder:
    def __init__(self, name: str):
        self.name = name
        self.children: List[Union[File, "Folder"]] = []

    def append(self, item: Union[File, "Folder"]):
        for child in self.children:
            if isinstance(child, Folder) and child.name == item.name:
                raise Exception(
                    f"Folder '{item.name}' already exists in '{self.name}', skipping."
                )

            elif isinstance(child, File) and child.name == item.name:
                raise Exception(
                    f"File '{item.name}' already exists in '{self.name}', skipping."
                )

        self.children.append(item)

    def extend(self, items: List[Union[File, "Folder"]]):
        for item in items:
            self.append(item)

    def create(self, path: Union[str, Path] = ""):
        full_path = Path(path).absolute() if path == "." else Path(path, self.name)
        if not full_path.exists():
            full_path.mkdir(exist_ok=True, parents=True)
        else:
            raise Exception(f"Folder {self.name} in {full_path} already exists.")

        for child in self.children:
            child.create(full_path)

    def insert(self, path: Union[str, Path]):
        full_path = Path(path).absolute()
        print(full_path)
        if not full_path.exists():
            raise Exception(f"Folder {full_path} does not exist.")

        for child in self.children:
            if isinstance(child, Folder):
                child.insert(full_path.joinpath(child.name))
            else:
                child.create(full_path)
