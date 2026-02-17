import yt_dlp
import logging
from pathlib import Path


DEFAULT_FORMAT = "mp4"
LOG_LEVEL = logging.DEBUG

my_downloads = Path.home().joinpath('Downloads').resolve()

class Downloader:
    def __init__(self):
        self.format = None
        self.options = dict()
        logging.basicConfig(level=LOG_LEVEL)
        self.logger = logging.getLogger(__name__)

        self.options["paths"] = {"downloads": str(Path(my_downloads).joinpath("yt-dlp-downloads"))}
        print(self.options['paths'])
        self.set_file_format(DEFAULT_FORMAT)
        self.logger.debug("Downloader initialized")

    
    def set_dl_path(self, entry_path):
        if str(entry_path) != self.options["paths"]["downloads"]:
            self.options["paths"]["downloads"] = str(entry_path)
            self.logger.debug("New path set: %s", str(entry_path))




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
                self.logger.debug("Format set to: mp3")
            else:
                self.options["acodec"] = None
                self.options["format"] = "mp4"
                self.options["postprocessors"] = []
                self.logger.debug("Format set to: mp4")



    def download_url(self, url):
        with  yt_dlp.YoutubeDL(self.options) as dl: # type: ignore
            try:
                errorcode = dl.download(url)
            except yt_dlp.utils.DownloadError as e: # type: ignore
                return e.msg
            self.logger.debug("Download failed" if errorcode else "Download successful")
        return ""
    

