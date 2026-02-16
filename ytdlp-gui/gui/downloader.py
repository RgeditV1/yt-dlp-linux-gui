import yt_dlp
from pathlib import Path


DEFAULT_FORMAT = "mp4"
DEFAULT_DOWNLOAD_DIR = "downloads"


class Downloader:
    def __init__(self):
        self.selection = DEFAULT_FORMAT
        self.paths = dict()

        self.paths["home"] = str(Path.cwd() / DEFAULT_DOWNLOAD_DIR)
        self.options = self.get_options()
        self.ytdl = yt_dlp.YoutubeDL(self.options)



    def get_options(self):
    
        if self.selection == "mp3":
            return {
                'paths': self.paths,
                'acodec': 'mp3',
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }]
            } 
        else:
            return {
                'paths': self.paths,
                'format': "mp4"
                }

    def download_url(self, url):
        errorcode = self.ytdl.download(url)
        print("Download failed" if errorcode else "Download successful")
    

