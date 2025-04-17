# Image & Video Converter

A simple, modern Python GUI app to convert videos (MP4 to WebM) and images (PNG/JPEG to WebP) using FFmpeg.

## Features

- Convert MP4 (and other videos) to compressed WebM (VP9)
- Convert PNG, JPEG, BMP, TIFF images to WebP
- Simple, modern UI (Tkinter)
- Compression and scaling for videos
- Windows and Linux support

## Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (must be installed and in your system PATH)

## Installation

1. **Install Python**  
   Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install FFmpeg**

   - Download the Windows build from [FFmpeg Download](https://ffmpeg.org/download.html).
   - Extract the ZIP.
   - Add the `bin` folder (containing `ffmpeg.exe`) to your Windows PATH:
     - Press `Win + S`, search for "Environment Variables".
     - Edit the `Path` variable and add the path to the `bin` folder.

3. **Clone or Download this Repository**

4. **Install Python requirements**  
   Open a terminal (cmd or PowerShell) in the project folder and run:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the app:
   ```
   python main.py
   ```
2. Select a file (image or video).
3. Choose the output format.
4. Click "Convert".

## Notes

- If FFmpeg is not found, the app will show an error and exit.
- Output files are saved in the same folder as the input.

---

**Made with Python & FFmpeg**
