import sys
from pathlib import Path


def resource_path(relative: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        # src/utils/paths.py -> <root>/src/utils/paths.py => root = parents[2]
        base = Path(__file__).resolve().parents[2]

    return str(base / relative)