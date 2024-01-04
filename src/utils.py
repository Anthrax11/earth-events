import os
from pathlib import Path
from datetime import datetime


def get_project_root(parents: int = 1) -> str:
    return str(Path(__file__).parents[parents])

def get_absolute_path(relative_path: str, *args, parents: int = 1) -> str:
    return os.path.join(
        get_project_root(parents),
        relative_path.strip(os.path.sep),
        *args
        )

def get_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def get_date() -> str:
    return datetime.now().strftime("%Y%m%d")

def obj_from_text(object_path: str) -> object:
    pass