# YTDLP UI Edition

A modern graphical interface for downloading YouTube videos and audio using **yt-dlp** and **CustomTkinter**.

Built in Python with a modular architecture and currently in a **stable phase**.

## Now You Can Download From AUR
```bash
yay -s yt-dlp-gui
```

---

## 📌 Project Status

**Stable**

The application currently:

- Downloads videos in **MP4** format  
- Downloads audio in **MP3** format  
- Allows custom download directory selection  
- Sends system notifications  
- Handles resource paths correctly in development  

---

##  Project Structure
```bash
ytdlp_gui/
│
├── core/
│   └── downloader.py
│
├── gui/
│   ├── ui.py
│   └── utils.py
│
├── img/
├── fonts/
│
└── YTDLP.py
```
- **core/** → Download logic (yt-dlp integration)  
- **gui/** → Graphical interface and utilities  
- **img / fonts/** → Static resources used by the UI  

---

## Installation (Recommended)

Instead of installing dependencies manually, simply run:
```bash
chmod +x setup.sh  
./setup.sh  
```
The setup script will automatically install all required dependencies and prepare the project.

### Windows

PowerShell:
```powershell
.\setup.ps1
```
If PowerShell blocks scripts:
```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

CMD:
```bat
setup.cmd
```

---

## ▶Running the Application

After running the setup script:
```bash
python ytdlp_gui/YTDLP.py  
```
---

## Features

- Modern dark-mode UI (CustomTkinter)  
- MP3 extraction using FFmpeg  
- Automatic download directory creation  
- Input validation before download  
- System notifications for download status  
- Clean separation between UI and core logic  

---

## How It Works

- The `Downloader` class dynamically configures yt-dlp options.
- Audio mode uses FFmpeg post-processing.
- The UI validates fields before starting downloads.
- A smart `resource_path()` function ensures proper asset loading.

---

## Main Dependencies

- yt-dlp  
- customtkinter  
- pillow  
- plyer  

(All installed automatically via `setup.sh`.)

---

##  Future Improvements

- Real-time download progress bar  
- Playlist support  
- Persistent configuration  
- Additional format options  

---

## 👤 Author

Developed by **RgeditV1**
and **RowanDavitt**

---
