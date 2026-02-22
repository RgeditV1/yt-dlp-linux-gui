import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    """
    Devuelve la ruta correcta tanto en desarrollo
    como cuando está compilado con PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path # type: ignore
    return Path(__file__).resolve().parent.parent / relative_path