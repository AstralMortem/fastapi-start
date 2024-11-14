from fastapi_start.core.asgi import get_asgi
from pathlib import Path
import os


BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR.joinpath("core", "config.toml")
os.environ.setdefault("SETTINGS_MODULE", str(CONFIG_PATH))
os.environ.setdefault("BASE_DIR", f"@path {BASE_DIR}")

app = get_asgi()

