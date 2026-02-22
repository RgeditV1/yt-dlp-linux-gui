import sys
import platform
import customtkinter as ctk
from ytdlp_gui.gui.ui import Ui
from ytdlp_gui.gui.utils import resource_path
from PIL import Image, ImageTk


class YTDLP(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YTDLP UI EDITION")
        self.geometry("400x500")
        self.resizable(False, False)

        self._set_app_icon()

        ctk.set_appearance_mode("dark")
        Ui(self)

    # =========================
    # Soporte multiplataforma para iconos
    # =========================
    def _set_app_icon(self):
        system = platform.system()

        try:
            if system == "Windows":
                # Windows soporta mejor .ico
                ico_path = resource_path("img/icon.ico")
                self.iconbitmap(ico_path)

                # También cargar png como respaldo visual
                png_path = resource_path("img/icon.png")
                icon_image = ImageTk.PhotoImage(Image.open(png_path))
                self.iconphoto(True, icon_image) # type: ignore
                self._icon_image = icon_image  # evitar garbage collection

            else:
                # Linux usa mejor png
                png_path = resource_path("img/icon.png")
                icon_image = ImageTk.PhotoImage(Image.open(png_path))
                self.iconphoto(True, icon_image) # type: ignore
                self._icon_image = icon_image

        except Exception as e:
            print(f"[WARNING] Could not load icon: {e}")


if __name__ == "__main__":
    app = YTDLP()
    app.mainloop()