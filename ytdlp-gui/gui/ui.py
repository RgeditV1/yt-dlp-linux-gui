import customtkinter as ctk
import webbrowser
from pathlib import Path
from PIL import Image, ImageDraw
from functools import wraps
import downloader

imgPTH = Path.cwd() / "img" / "yt_logo.png"
font = Path.cwd() / 'fonts' / 'Super Wonder.ttf'
mp3_icon = Path.cwd() / 'img' / 'mp3_icon.png'
mp4_icon = Path.cwd() / 'img' / 'mp4_icon.png'
download_icon = Path.cwd() / 'img' / 'download.png'
my_icon = Path.cwd() / 'img'/ 'profile.jpg'
ruta = Path.cwd()


class Ui():
    def __init__(self, main_frame):
        self.main_frame = main_frame
        ctk.FontManager.load_font(str(font))
        self.header()
        self.content()
        self.dl = downloader.Downloader()
    
    def header(self):
        img = Image.open(imgPTH)
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

    def formato(self):
        #------------------------
        # FORMATO
        #-----------------------
        mp3ico = Image.open(mp3_icon)
        self.mp3_ico = ctk.CTkImage(light_image=mp3ico,
                                    dark_image=mp3ico, size=(25,25))
        mp4ico = Image.open(mp4_icon)
        self.mp4_ico = ctk.CTkImage(light_image=mp4ico,
                                    dark_image=mp4ico, size=(25,25))
        
        self.formato_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent')
        self.formato_frame.pack(padx=(10,5),pady=(10,10), fill='x')

        self.formato_label = ctk.CTkLabel(self.formato_frame, text='Formato', font=('Super Wonder',20))
        self.formato_label.pack()

        self.mp3_btn = ctk.CTkButton(self.formato_frame, image=self.mp3_ico ,text='Audio\nMP3', width=120,fg_color='transparent',
                                     border_width=1, border_spacing=0,border_color='blue', hover_color='gray',command=self.mp3_pressed)
        self.mp3_btn.pack(side='left', padx=(5,5))

        self.mp4_btn = ctk.CTkButton(self.formato_frame, image=self.mp4_ico,text='Video\nMP4',
                                     fg_color="transparent", width=120,border_spacing=0,border_width=1,
                                     border_color='red', hover_color='gray',command=self.mp4_pressed)
        self.mp4_btn.pack(padx=(5,5))
    

    @staticmethod
    def redondear_img(func):
        @wraps(func)
        def wrapper(self):
            size = (50, 50)
            img = Image.open(my_icon).resize(size).convert("RGBA")
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


    def guardar(self):
        self.mostrar_ruta = ctk.StringVar(value=str(ruta))
        
        #Nota para el futuro, utilizar self.mostrar_ruta.set('nuevo texto') si quiero cambiar texto del label
        
        self.guardar_frame = ctk.CTkFrame(self.content_frame, fg_color='transparent', border_width=1)
        self.guardar_frame.pack(fill='y', pady=(15,15))

        self.label_ruta = ctk.CTkLabel(self.guardar_frame, textvariable=self.mostrar_ruta)
        self.label_ruta.pack()



        self.guardar_btn = ctk.CTkButton(self.guardar_frame, text='Guardar en',
                                         border_spacing=0, width=90, fg_color='transparent',
                                         border_width=1, border_color='gray')
        self.guardar_btn.pack()


    def content(self):
        self.content_frame = ctk.CTkFrame(self.main_frame, width=300, border_width=1)
        self.content_frame.pack(pady=(20,10))
        #self.content_frame.pack_propagate(False)

        self.url()
        self.formato()
        self.guardar()

        download = Image.open(download_icon)
        self.download_ico = ctk.CTkImage(light_image=download,
                                         dark_image=download,
                                         size=(25,25))
        self.descargar_btn = ctk.CTkButton(self.content_frame, image=self.download_ico, height=35,
                                           text='Iniciar Descarga', fg_color='transparent', border_width=1,
                                           border_color='green', hover_color='gray',command=self.descargar_pressed)
        self.descargar_btn.pack()
        
        self.show_profile()

    def descargar_pressed(self):
        self.dl.download_url(self.url_entry.get())

    def mp4_pressed(self):
        self.dl.set_file_type("mp4")

    def mp3_pressed(self):
        self.dl.set_file_type("mp3")
