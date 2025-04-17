import subprocess
import os

def convert_video_to_webm(input_path, output_path, scale=720, fps=60, crf=42):
    cmd = [
        "ffmpeg", "-i", input_path, "-an",
        "-vf", f"scale={scale}:-1,fps={fps}",
        "-c:v", "libvpx-vp9", "-crf", str(crf),
        output_path
    ]
    return subprocess.run(cmd, capture_output=True)

def convert_image_to_webp(input_path, output_path):
    cmd = [
        "ffmpeg", "-i", input_path, output_path
    ]
    return subprocess.run(cmd, capture_output=True)

def is_video(filename):
    return os.path.splitext(filename)[1].lower() in [".mp4", ".mov", ".avi", ".mkv"]

def is_image(filename):
    return os.path.splitext(filename)[1].lower() in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]
