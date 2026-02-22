import yt_dlp
from pathlib import Path
from plyer import notification


DEFAULT_FORMAT = "mp4"

class Downloader:
    def __init__(self):
        self.format = None
        self.options = dict()

        self.options["paths"] = {"home": None}
        self.options["outtmpl"] = "%(title)s.%(ext)s" #this not include the id in file name
        self.set_file_format(DEFAULT_FORMAT)

    
    def set_dl_path(self, entry_path):
        if str(entry_path) != self.options["paths"]["home"]:
            self.options["paths"]["home"] = str(entry_path)
            Path(self.options['paths']['home']).mkdir(parents=True, exist_ok=True)




    def set_file_format(self, file_format):
        if file_format != self.format:
            self.format = file_format
    
            if file_format == "mp3":
                # based on code from https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extract-audio
                self.options["format"] = None
                self.options["acodec"] = "mp3"
                self.options["postprocessors"]= [
                    {  # Extract audio using ffmpeg
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                    }]
            else:
                self.options["acodec"] = None
                self.options["format"] = "mp4"
                self.options["postprocessors"] = []



    def send_notify(self, message=None):
        notification.notify(
                    title='Status',
                    message=message,
                    app_name="YTDLP UI EDITION",
                    timeout=5,
                    toast=True
                ) # type: ignore

    def download_url(self, url):
        with  yt_dlp.YoutubeDL(self.options) as dl: # type: ignore
            try:
                self.send_notify('Download started')
                errorcode = dl.download(url)
            except yt_dlp.utils.DownloadError as e: # type: ignore
                return self.send_notify(e.msg)
            if errorcode:
                self.send_notify('Download Failed')
            else:
                self.send_notify('Download Successful')

        return ""
    

