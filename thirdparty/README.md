# thirdparty

Esta carpeta se usa para binarios externos requeridos por la app (principalmente FFmpeg).

Estructura esperada:

- `thirdparty/windows/ffmpeg.exe`
- `thirdparty/windows/ffprobe.exe`
- `thirdparty/linux/ffmpeg`
- `thirdparty/linux/ffprobe`

Nota:
- Estos binarios no se versionan en git (por tamaño). Se descargan en CI y se incluyen en el ZIP/Release.

Descarga manual (opcional):
- Linux: `python scripts/fetch_ffmpeg.py --platform linux`
- Windows: `python scripts/fetch_ffmpeg.py --platform windows` (o `python scripts/fetch_ffmpeg_windows.py`)
