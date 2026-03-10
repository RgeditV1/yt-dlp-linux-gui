# thirdparty

Esta carpeta se usa para binarios externos requeridos por la app (principalmente FFmpeg).

Estructura esperada:

- `thirdparty/windows/ffmpeg.exe`
- `thirdparty/windows/ffprobe.exe`
- `thirdparty/linux/ffmpeg`
- `thirdparty/linux/ffprobe`

Nota:
- Estos binarios no se versionan en git (por tamanio). Se descargan en CI y se incluyen en el ZIP/Release.

