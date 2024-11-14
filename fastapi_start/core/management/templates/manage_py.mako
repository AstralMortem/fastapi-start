#!/usr/bin/env python
from pathlib import Path
import os


def main():
    BASE_DIR = Path(__file__).parent
    CONFIG_PATH = BASE_DIR.joinpath("core", "config.toml")
    os.environ.setdefault("FASTAPI_SETTINGS_MODULE", str(CONFIG_PATH))
    os.environ.setdefault("FASTAPI_BASE_DIR", f"@path {BASE_DIR}")
    try:
        from fastapi_start.core.cli import cli_app
    except ImportError as exc:
        raise ImportError(
            "Could not import fastapi_start module, make sure you installed it."
        ) from exc
    cli_app()


if __name__ == "__main__":
    main()
