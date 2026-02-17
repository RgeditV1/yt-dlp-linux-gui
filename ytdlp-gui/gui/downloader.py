import yt_dlp
from pathlib import Path


DEFAULT_FORMAT = "mp4"
DEFAULT_DOWNLOAD_DIR = "downloads"


class Downloader:
    def __init__(self):
        self.format = DEFAULT_FORMAT
        self.paths = dict()

        self.paths["home"] = str(Path.cwd() / DEFAULT_DOWNLOAD_DIR)
        self.options = self.make_options()



    def make_options(self):

        options = dict()

        options["paths"] = self.paths
    
        if self.format == "mp3":
            # based on code from https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#extract-audio
            options["acodec"] = "mp3"
            options["postprocessors"]= [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }]
        else:
            options["format"] = "mp4"
        return options


    def download_url(self, url):
        with  yt_dlp.YoutubeDL(self.options) as dl:
            errorcode = dl.download(url)  
            print("Download failed" if errorcode else "Download successful")


    def set_file_type(self,file_format):
        if file_format != self.format:
            print("Format changed to: ", file_format)
            self.format = file_format
            self.options = self.make_options()

