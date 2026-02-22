from cx_Freeze import setup, Executable
import platform

# Detectar sistema operativo para elegir base correcto
if platform.system() == "Windows":
    base = "Win32GUI"  # GUI sin consola en Windows
else:
    base = "gui"       # GUI multiplataforma en Linux/macOS

# Opciones de build
build_exe_options = {
    "packages": [
        "os",
        "sys",
        "logging",
        "webbrowser",
        "pathlib",
        "functools",
        "customtkinter",
        "PIL",
        "plyer",
        "yt_dlp"
    ],
    "include_files": [
        ("ytdlp_gui/img", "img"),       # Carpeta de imágenes
        ("ytdlp_gui/fonts", "fonts"),   # Carpeta de fuentes
        "README.md",
        "LICENSE",
        "preview.png"
    ],
    "excludes": []
}

setup(
    name="YTDLP-GUI-RgeditV1",
    version="1.0",
    description="Graphical interface for yt-dlp with desktop notifications",
    author="RgeditV1",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "ytdlp_gui/YTDLP.py",       # Script principal
            base=base,
            icon="ytdlp_gui/img/icon.jpg"  # Ícono de la ventana
        )
    ]
)
