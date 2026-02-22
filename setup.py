from cx_Freeze import setup, Executable
import sys
import platform
from pathlib import Path

# =========================
# Detectar sistema operativo
# =========================
system = platform.system()

if system == "Windows":
    base = "Win32GUI"
    icon_path = "ytdlp_gui/img/icon.ico"
else:
    base = None  # En Linux no se necesita base especial
    icon_path = "ytdlp_gui/img/icon.png"

# =========================
# Archivos adicionales
# =========================
include_files = [
    ("ytdlp_gui/img", "img"),
    ("ytdlp_gui/fonts", "fonts"),
    "README.md",
    "LICENSE",
]

# Solo incluir desktop file en Linux
if system != "Windows":
    include_files.append("yt-dlp-gui.desktop")

# =========================
# Opciones de build
# =========================
build_exe_options = {
    "packages": [
        "customtkinter",
        "PIL",
        "plyer",
        "yt_dlp"
    ],
    "include_files": include_files,
    "include_msvcr": True,  # IMPORTANTE para Windows
    "optimize": 1,
    "excludes": [
        "tkinter.test",
        "unittest",
        "test"
    ],
}

# =========================
# Setup
# =========================
setup(
    name="YTDLP-GUI-RgeditV1",
    version="1.0.0",
    description="Graphical interface for yt-dlp with desktop notifications",
    author="RgeditV1",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "ytdlp_gui/YTDLP.py",
            base=base,
            icon=icon_path,
            target_name="YTDLP-GUI"
        )
    ]
)