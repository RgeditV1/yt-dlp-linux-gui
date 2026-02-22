import customtkinter as ctk
from ytdlp_gui.gui.ui import Ui
from ytdlp_gui.gui.utils import resource_path
from PIL import Image, ImageTk

class YTDLP(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YTDLP UI EDITION")
        self.geometry('400x500')
        self.resizable(False, False)
        icon_path = resource_path("img/icon.png")
        icon_image = ImageTk.PhotoImage(Image.open(icon_path))
        self.iconphoto(True, icon_image) # type: ignore
        ctk.set_appearance_mode('dark')

        Ui(self)



if __name__ == '__main__':
    app = YTDLP()
    app.mainloop()