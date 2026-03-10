import yt_dlp
from pathlib import Path
from plyer import notification

DEFAULT_FORMAT = "mp4"
DEFAULT_RESOLUTION = "HD(720p)"

class Downloader:
    def __init__(self):
        self.format = None
        self.extract_thumbnail = False
        self.options = dict()

        self.options["paths"] = {"home": None}
        self.options["outtmpl"] = "%(title)s.%(ext)s" #this not include the id in file name
        self.set_file_format(DEFAULT_FORMAT, DEFAULT_RESOLUTION)

    
    def set_dl_path(self, entry_path):
        if str(entry_path) != self.options["paths"]["home"]:
            self.options["paths"]["home"] = str(entry_path)
            Path(self.options['paths']['home']).mkdir(parents=True, exist_ok=True)




    def set_file_format(self, file_format, file_resolution=None):
        self.format = file_format
        self._apply_format_options(file_format, file_resolution)

    def set_extract_thumbnail(self, enabled):
        self.extract_thumbnail = bool(enabled)

    def _apply_format_options(self, file_format, file_resolution):
        # Reset options linked to media processing.
        self.options["writethumbnail"] = False
        self.options["postprocessors"] = []
        if file_format == "mp3":
            # based on code from https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extract-audio
            self.options["format"] = "bestaudio/best"
            self.options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ]
        else:
            resolution = {
                "4K(2160p)"     : "2160",
                "Full HD(1080p)": "1080",
                "HD(720p)"      : "720",
                "SD(480p)"      : "480"
            }
            pixel = resolution.get(file_resolution, resolution[DEFAULT_RESOLUTION])
            self.options.update({
                'format': f'bestvideo[height<={pixel}][ext=mp4]+bestaudio[ext=m4a]/best[height<={pixel}]',
                'merge_output_format': 'mp4'
            })
            self.options["postprocessors"].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            })



    def send_notify(self, message=None):
        try:
            notification.notify(
                        title='Status',
                        message=message,
                        app_name="YTDLP UI EDITION",
                        timeout=5,
                        toast=True
                    ) # type: ignore
        except: pass

    def download_url(self, url, progress_callback=None, status_callback=None):
        options = dict(self.options)
        options["postprocessors"] = list(self.options.get("postprocessors", []))

        if self.extract_thumbnail:
            options["writethumbnail"] = True
            options["postprocessors"].append(
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg",
                }
            )

        options["progress_hooks"] = [self._build_progress_hook(progress_callback, status_callback)]

        try:
            with yt_dlp.YoutubeDL(options) as dl: # type: ignore
                self.send_notify('Download started')
                errorcode = dl.download([url])
                if errorcode:
                    self.send_notify('Download Failed')
                    if status_callback:
                        status_callback("Descarga fallida")
                    return "download failed"
                self.send_notify('Download Successful')
                if progress_callback:
                    progress_callback(1.0)
                if status_callback:
                    if self.extract_thumbnail:
                        status_callback("Imagen JPG extraida correctamente")
                    else:
                        status_callback("Descarga completada")
        except yt_dlp.utils.DownloadError as e: # type: ignore
            if status_callback:
                status_callback(f"Error: {e.msg}")
            self.send_notify(e.msg)
            return str(e.msg)
        except Exception as e:
            if status_callback:
                status_callback(f"Error inesperado: {e}")
            self.send_notify("Download Failed")
            return str(e)

        return ""

    def _build_progress_hook(self, progress_callback, status_callback):
        def hook(data):
            if data.get("status") == "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate")
                downloaded = data.get("downloaded_bytes", 0)
                if total and progress_callback:
                    progress_callback(min(downloaded / total, 1.0))
                if status_callback:
                    status_callback("Descargando...")

            if data.get("status") == "finished":
                if status_callback:
                    if self.extract_thumbnail:
                        status_callback("Procesando miniatura...")
                    else:
                        status_callback("Procesando archivo...")
        return hook
    
