import customtkinter as ctk
from ui import Ui

class YTDLP(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YTDLP UI EDITION")
        self.geometry('400x500')
        self.resizable(False, False)
        ctk.set_appearance_mode('system')

        Ui(self)



if __name__ == '__main__':
    app = YTDLP()
    app.mainloop()