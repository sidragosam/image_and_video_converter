import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import shutil
from converter import convert_video_to_webm, convert_image_to_webp, is_video, is_image

class ConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image & Video Converter")
        self.geometry("440x270")
        self.resizable(True, True)
        self.configure(bg="#23272f")
        self.input_path = ""
        self.output_path = ""
        self.create_widgets()
        self.check_ffmpeg()

    def check_ffmpeg(self):
        if shutil.which("ffmpeg") is None:
            messagebox.showerror(
                "FFmpeg Not Found",
                "FFmpeg is not installed or not in your PATH.\n\n"
                "Please download it from https://ffmpeg.org/download.html and add it to your system PATH."
            )
            self.destroy()

    def create_widgets(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 11), padding=7, background="#3a3f4b", foreground="#fff")
        style.map('TButton', background=[('active', '#4e5463')])
        style.configure('TLabel', background="#23272f", foreground="#fff", font=('Segoe UI', 11))
        style.configure('TEntry', font=('Segoe UI', 11))
        style.configure('TFrame', background="#23272f")

        main_frame = ttk.Frame(self, padding=(18, 12, 18, 12))
        main_frame.pack(fill="both", expand=True)

        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(file_frame, text="Select file to convert:").grid(row=0, column=0, sticky="w")
        self.file_entry = ttk.Entry(file_frame, width=32)
        self.file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(2, 0))
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=1, column=1, sticky="ew", pady=(2, 0))
        file_frame.columnconfigure(0, weight=1)

        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(format_frame, text="Output format:").grid(row=0, column=0, sticky="w")
        self.format_var = tk.StringVar(value="webp (image)")
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, state="readonly",
                                         values=["webp (image)", "webm (video)"], width=18)
        self.format_combo.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate", length=260)
        self.progress.pack(pady=(8, 0))

        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=('Segoe UI', 10, 'italic'))
        self.status_label.pack(pady=(6, 0))

        # Convert button
        convert_btn = ttk.Button(main_frame, text="Convert", command=self.start_conversion)
        convert_btn.pack(pady=(14, 0), ipadx=10)

    def browse_file(self):
        filetypes = [("All files", "*.*")]
        path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if path:
            self.input_path = path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)

    def start_conversion(self):
        input_path = self.file_entry.get()
        if not input_path or not os.path.isfile(input_path):
            messagebox.showerror("Error", "Please select a valid file.")
            return
        self.progress.start(10)
        self.status_label.config(text="Starting conversion...")
        self.disable_widgets()
        threading.Thread(target=self.convert, daemon=True).start()

    def convert(self):
        input_path = self.file_entry.get()
        ext = os.path.splitext(input_path)[1].lower()
        fmt = self.format_var.get()
        out_dir = os.path.dirname(input_path)
        base = os.path.splitext(os.path.basename(input_path))[0]

        if is_video(input_path) and "webm" in fmt:
            output_path = os.path.join(out_dir, base + ".webm")
            self.set_status("Converting video...")
            result = convert_video_to_webm(input_path, output_path)
        elif is_image(input_path) and "webp" in fmt:
            output_path = os.path.join(out_dir, base + ".webp")
            self.set_status("Converting image...")
            result = convert_image_to_webp(input_path, output_path)
        else:
            self.set_status("File type and output format do not match.")
            self.progress.stop()
            self.enable_widgets()
            messagebox.showerror("Error", "File type and output format do not match.")
            return

        if result.returncode == 0:
            self.set_status(f"Success! Saved: {output_path}")
        else:
            self.set_status("Conversion failed.")
            messagebox.showerror("Error", result.stderr.decode())
        self.progress.stop()
        self.enable_widgets()

    def set_status(self, msg):
        self.status_label.config(text=msg)

    def disable_widgets(self):
        self.file_entry.config(state="disabled")
        self.format_combo.config(state="disabled")

    def enable_widgets(self):
        self.file_entry.config(state="normal")
        self.format_combo.config(state="readonly")

if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()
