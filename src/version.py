from pathlib import Path

_PATH_TO_VERSION_FILE = Path(__file__).parents[1] / "VERSION"
__version__ = _PATH_TO_VERSION_FILE.read_text(encoding="utf-8").strip()
"""Package version"""
