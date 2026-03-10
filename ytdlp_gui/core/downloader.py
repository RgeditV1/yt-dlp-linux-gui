import yt_dlp
from pathlib import Path
from plyer import notification
import os
import shutil
import sys

DEFAULT_FORMAT = "mp4"
DEFAULT_RESOLUTION = "HD(720p)"

class Downloader:
    def __init__(self):
        self.format = None
        self.extract_thumbnail = False
        self.video_resolution = DEFAULT_RESOLUTION
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
        if file_format == "mp4":
            self.video_resolution = file_resolution or DEFAULT_RESOLUTION
        self._apply_format_options(file_format, file_resolution)

    def set_extract_thumbnail(self, enabled):
        self.extract_thumbnail = bool(enabled)

    @staticmethod
    def _app_base_dir():
        # Frozen build: sys.executable points to the generated exe
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        # Source: repo root (ytdlp_gui/core/downloader.py -> parents[2])
        return Path(__file__).resolve().parents[2]

    @classmethod
    def _thirdparty_bin_dir(cls):
        base = cls._app_base_dir()
        thirdparty = base / "thirdparty"
        if os.name == "nt":
            return thirdparty / "windows"
        return thirdparty / "linux"

    @classmethod
    def _find_ffmpeg_location(cls):
        """
        Returns a path that yt-dlp can use as ffmpeg location, or None if not found.
        Preference order:
        1) Bundled binaries in `thirdparty/<platform>/`
        2) System PATH (`shutil.which`)
        """
        bin_dir = cls._thirdparty_bin_dir()
        if os.name == "nt":
            ffmpeg_bin = bin_dir / "ffmpeg.exe"
            ffprobe_bin = bin_dir / "ffprobe.exe"
        else:
            ffmpeg_bin = bin_dir / "ffmpeg"
            ffprobe_bin = bin_dir / "ffprobe"

        if ffmpeg_bin.exists():
            # yt-dlp accepts a directory; this allows finding ffprobe too.
            if ffprobe_bin.exists():
                return str(bin_dir)
            return str(ffmpeg_bin)

        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            return ffmpeg
        return None

    def _apply_format_options(self, file_format, file_resolution):
        # Reset options linked to media processing.
        self.options["writethumbnail"] = False
        self.options["postprocessors"] = []
        self.options.pop("ffmpeg_location", None)
        self.options.pop("merge_output_format", None)

        if file_format == "mp3":
            # based on code from https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extract-audio
            self.options["format"] = "bestaudio/best"
            ffmpeg_location = self._find_ffmpeg_location()
            if ffmpeg_location:
                self.options["ffmpeg_location"] = ffmpeg_location
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
            ffmpeg_location = self._find_ffmpeg_location()

            if ffmpeg_location:
                # Tiered behavior:
                # - SD/HD/FHD stay capped (never exceed selected height)
                # - 4K: if 2160 isn't available, pick the highest available <= 2160 (1440/1080/etc)
                fmt = (
                    f"bestvideo[height={pixel}][ext=mp4]+bestaudio[ext=m4a]/"
                    f"bestvideo[height<={pixel}][ext=mp4]+bestaudio[ext=m4a]/"
                    f"bestvideo[height={pixel}]+bestaudio/"
                    f"bestvideo[height<={pixel}]+bestaudio/"
                    f"best[height={pixel}][ext=mp4]/"
                    f"best[height<={pixel}][ext=mp4]/"
                    f"best[height={pixel}]/"
                    f"best[height<={pixel}]/"
                    f"worst"
                )
                self.options.update({
                    "ffmpeg_location": ffmpeg_location,
                    "format": fmt,
                    "merge_output_format": "mp4",
                    "abort_on_unavailable_fragments": True,
                })
            else:
                # No FFmpeg: progressive MP4 only, still capped.
                self.options.update({
                    "format": (
                        f"best[height={pixel}][ext=mp4]/"
                        f"best[height<={pixel}][ext=mp4]/"
                        f"worst[ext=mp4]/worst"
                    )
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
        # Re-evaluate MP4 options at download time (FFmpeg may appear after packaging).
        if self.format == "mp4":
            self._apply_format_options("mp4", self.video_resolution)

        ffmpeg_location = self.options.get("ffmpeg_location") or self._find_ffmpeg_location()
        if self.format == "mp3" and not ffmpeg_location:
            msg = "FFmpeg no detectado: MP3 requiere FFmpeg."
            if status_callback:
                status_callback(msg)
            return msg
        # For HD+ in Windows builds we want deterministic behavior; require FFmpeg for >= 720p.
        if self.format == "mp4" and self.video_resolution != "SD(480p)" and not ffmpeg_location:
            msg = "FFmpeg no detectado: para 720p/1080p/4K se requiere FFmpeg (thirdparty/windows o PATH)."
            if status_callback:
                status_callback(msg)
            return msg

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
    
