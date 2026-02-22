import customtkinter as ctk
import webbrowser
from pathlib import Path
from PIL import Image, ImageDraw
from functools import wraps
from ytdlp_gui.core.downloader import Downloader
from plyer import notification
from ytdlp_gui.gui.utils import resource_path



class Ui:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        BASE_DIR = resource_path("")

        self._paths = {
            "download_dir": Path.home() / "Downloads" / "yt-dlp-downloads",
            "entry_path": Path(),
            "logo": BASE_DIR / "img" / "yt_logo.png",
            "font": BASE_DIR / "fonts" / "Super Wonder.ttf",
            "mp3_icon": BASE_DIR / "img" / "mp3_icon.png",
            "mp4_icon": BASE_DIR / "img" / "mp4_icon.png",
            "download_icon": BASE_DIR / "img" / "download.png",
            "my_icon": BASE_DIR / "img" / "profile.jpg",
        }

        if not self._paths["download_dir"].exists():
            self._paths["download_dir"].mkdir(parents=True, exist_ok=True)

        ctk.FontManager.load_font(str(self._paths["font"]))

        self.dl = Downloader()

        self.header()
        self.content()

        self.set_button_status(self.mp4_btn)


    def get_path_list(self, key):
        if key:
            return self._paths.get(key)
        return self._paths

    def set_path(self, key, value):
        self._paths[key] = value

#Notification Area
    def notify(self,msg):
        notification.notify(
            title='Status',
            message=msg,
            app_name="YTDLP UI EDITION",
            timeout=5,
            toast=True
        ) # type: ignore
                
    def header(self):
        img = Image.open(str(self.get_path_list('logo')))
        self.logo = ctk.CTkImage(light_image=img,
                            dark_image=img, size=(40,30))
        
        Label=ctk.CTkLabel(self.main_frame, image=self.logo, text='Downloader',
                           font=('Super Wonder',30),compound='left', padx=5)
        Label.pack(pady=(10,10))

        self.under_line = ctk.CTkFrame(self.main_frame, width=300, height=3, border_width=1)
        self.under_line.pack()


    def url(self):

        #------------------------
        # URL
        #-----------------------
        self.url_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.url_frame.pack(padx=(10,5),pady=(10,10), fill='x')

        url_label = ctk.CTkLabel(self.url_frame, text='URL DE YOUTUBE', font=('Super Wonder', 20))
        url_label.pack(pady=(0,0), padx=(0,5), anchor='w')

        self.url_entry = ctk.CTkEntry(self.url_frame, width=300, height=30,
                                 placeholder_text='https://www.youtube.com/watch?v=')
        self.url_entry.pack(padx=(0,5))

    def format(self):
        #------------------------
        # FORMAT
        #-----------------------
        mp3ico = Image.open(str(self.get_path_list('mp3_icon')))
        self.mp3_ico = ctk.CTkImage(light_image=mp3ico,
                                    dark_image=mp3ico, size=(25,25))
        mp4ico = Image.open(str(self.get_path_list('mp4_icon')))
        self.mp4_ico = ctk.CTkImage(light_image=mp4ico,
                                    dark_image=mp4ico, size=(25,25))
        
        self.format_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.format_frame.pack(padx=(10,5),pady=(10,10), fill='x')

        self.format_label = ctk.CTkLabel(self.format_frame, text='Formato', font=('Super Wonder',20))
        self.format_label.pack()

        self.mp3_btn = ctk.CTkButton(self.format_frame, image=self.mp3_ico,
                                     text='Audio\nMP3', width=120,fg_color='transparent',
                                     border_width=1, border_spacing=0,
                                     border_color='blue', hover_color='gray',
                                     command=lambda:[self.mp3_pressed(), self.set_button_status(self.mp3_btn)])
        self.mp3_btn.pack(side='left', padx=(5,5))

        self.mp4_btn = ctk.CTkButton(self.format_frame, image=self.mp4_ico,
                                     text='Video\nMP4', fg_color="transparent",
                                     width=120,border_spacing=0, border_width=1,
                                     border_color='red', hover_color='gray',
                                     command=lambda:[self.mp4_pressed(), self.set_button_status(self.mp4_btn)])
        self.mp4_btn.pack(padx=(5,5))
    

    @staticmethod
    def redondear_img(func):
        @wraps(func)
        def wrapper(self):
            size = (50, 50)
            img = Image.open(str(self.get_path_list('my_icon'))).resize(size).convert("RGBA")
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)

            img.putalpha(mask)

                # 👇 ahora sí pasamos la imagen procesada
            return func(self, img)

        return wrapper
    
    @redondear_img
    def show_profile(self, rounded_img):
        self.profile_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.profile_frame.pack(pady=(20,20))

        self.profile_img = ctk.CTkImage(
            light_image=rounded_img,
            dark_image=rounded_img,
            size=(50, 50)
        )

        label = ctk.CTkLabel(self.profile_frame, image=self.profile_img, text="")
        label.pack(side='left')

        def open_github(event=None):
            webbrowser.open("https://github.com/RgeditV1")

        self.github_label = ctk.CTkLabel(
            self.profile_frame,
            text="By RgeditV1",
            text_color="#3b82f6",   # azul tipo link
            cursor="hand2")

        self.github_label.pack()
        self.github_label.bind("<Button-1>", open_github)


    def save_file(self):

        #Use it for update Label Path
        self.show_path = ctk.StringVar(value=str(self.get_path_list('download_dir')))
        
        self.save_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.save_frame.pack(fill='y', pady=(15,15))

        self.entry_path = ctk.CTkEntry(self.save_frame, textvariable=self.show_path, width=300)
        self.entry_path.pack()

        self.save_btn = ctk.CTkButton(self.save_frame, text='Guardar en',
                                         border_spacing=0, width=90, fg_color='transparent',
                                         border_width=1, border_color='gray', command=self.save_pressed)
        self.save_btn.pack(pady=(5,5))


    def content(self):
        self.content_frame = ctk.CTkFrame(self.main_frame, width=300, border_width=1)
        self.content_frame.pack(pady=(20,10))
        #self.content_frame.pack_propagate(False)

        self.url()
        self.format()
        self.save_file()

        download = Image.open(str(self.get_path_list('download_icon')))
        self.download_ico = ctk.CTkImage(light_image=download,
                                         dark_image=download,
                                         size=(25,25))
        
        self.descargar_btn = ctk.CTkButton(self.content_frame, image=self.download_ico, height=35,
                                           text='Iniciar Descarga', fg_color='transparent', border_width=1,
                                           border_color='green', hover_color='gray',command=self.download_pressed) # type: ignore
        self.descargar_btn.pack()
        
        self.show_profile() # type: ignore

    def set_button_status(self, pressed):
        #set buttons fg default
        self.mp3_btn.configure(fg_color="transparent")
        self.mp4_btn.configure(fg_color="transparent")

        #if you find another beauty color, change it
        pressed.configure(fg_color="#1f6aa5")


    @staticmethod
    def validate_fields(func):
        @wraps(func)
        def wrapper(self):
            url = self.url_entry.get()
            self.set_path('entry_path', Path(self.entry_path.get()))
            valid = True
            if Path(self.get_path_list('entry_path')).exists():
                self.entry_path.configure(require_redraw=True, border_color="green")
                self.dl.set_dl_path(self.get_path_list('entry_path'))
            else:
                self.entry_path.configure(require_redraw=True, border_color="red")
                valid = False

            if len(url) == 0:
                self.notify('Please use a valid url')
                self.url_entry.configure(require_redraw=True, border_color="red")
                valid = False
            else:
                self.url_entry.configure(require_redraw=True, border_color="green")

            if not valid:
                return
            return func(self,url)
        return wrapper


    @validate_fields
    def download_pressed(self,url):
        if self.dl.download_url(url) != "":
            self.url_entry.configure(require_redraw=True, border_color="green")
        

    def mp4_pressed(self):
        self.dl.set_file_format("mp4")

    def mp3_pressed(self):
        self.dl.set_file_format("mp3")

    def save_pressed(self):
        select = ctk.filedialog.Directory(title="Choose download location")
        chosen = select.show()

        if isinstance(chosen, tuple): 
            chosen = chosen[0] if chosen else ""

        # update entry_path
        if chosen != "" and Path(chosen).exists():
            self.set_path("entry_path", Path(chosen))
        else:
            self.set_path("entry_path", self.get_path_list("download_dir"))

        final_path = str(self.get_path_list("entry_path"))

        self.entry_path.delete(0, "end")
        self.entry_path.insert(0, final_path)
        self.dl.set_dl_path(final_path)




