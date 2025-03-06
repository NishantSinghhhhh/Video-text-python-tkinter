#!/usr/bin/env python3

import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
import subprocess

REQUIRED_PACKAGES = ["requests", "pydub", "moviepy"]
missing_packages = []
for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg)
    except ImportError:
        missing_packages.append(pkg)

if missing_packages:
    root = tk.Tk()
    root.title("Missing Dependencies")
    root.geometry("800x200")
    label = tk.Label(root, text="The following packages are missing:\n" + ", ".join(missing_packages))
    label.pack(padx=20, pady=20)
    
    def install_dependencies():
        for pkg in missing_packages:
            subprocess.call([sys.executable, "-m", "pip", "install", pkg])
        messagebox.showinfo("Installation", "Dependencies installed.\nPlease restart the application.")
        root.destroy()
        sys.exit(0)
    
    install_btn = tk.Button(root, text="Install Dependencies", command=install_dependencies)
    install_btn.pack(pady=10)
    root.mainloop()

import traceback
from pydub import AudioSegment
import tempfile
import requests


class VideoTranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcription Tool")
        self.root.geometry("1900x1600")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.openai_api_key = "API_KEY"
        
        self.is_processing = False
        self.current_task = None
        self.error_log = []
        
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", padding=6, relief="flat", background="#3498db", foreground="black")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0")
        
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        title_label = ttk.Label(title_frame, text="Video Transcription Tool", font=("Arial", 18, "bold"))
        title_label.pack(side=tk.LEFT)
        
        file_frame = ttk.LabelFrame(main_frame, text="Select Video File", padding=10)
        file_frame.pack(fill=tk.X, pady=10)
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=50)
        file_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side=tk.RIGHT)
        
        options_frame = ttk.LabelFrame(main_frame, text="Transcription Options", padding=10)
        options_frame.pack(fill=tk.X, pady=10)
        self.speaker_diarization = tk.BooleanVar(value=False)
        speaker_check = ttk.Checkbutton(options_frame, text="Speaker Diarization", variable=self.speaker_diarization)
        speaker_check.pack(side=tk.LEFT, padx=10)
        self.auto_highlights = tk.BooleanVar(value=True)
        highlights_check = ttk.Checkbutton(options_frame, text="Auto Highlights", variable=self.auto_highlights)
        highlights_check.pack(side=tk.LEFT, padx=10)
        self.format_text = tk.BooleanVar(value=True)
        format_check = ttk.Checkbutton(options_frame, text="Format Text", variable=self.format_text)
        format_check.pack(side=tk.LEFT, padx=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        transcript_frame = ttk.Frame(notebook, padding=10)
        notebook.add(transcript_frame, text="Transcript")
        self.transcript_text = scrolledtext.ScrolledText(transcript_frame, wrap=tk.WORD, height=15)
        self.transcript_text.pack(fill=tk.BOTH, expand=True)
        processed_frame = ttk.Frame(notebook, padding=10)
        notebook.add(processed_frame, text="Processed Data")
        self.processed_text = scrolledtext.ScrolledText(processed_frame, wrap=tk.WORD, height=15)
        self.processed_text.pack(fill=tk.BOTH, expand=True)

        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor="w")
        status_label.pack(side=tk.LEFT, fill=tk.X)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, length=200, mode="determinate")
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        self.transcribe_button = ttk.Button(buttons_frame, text="Transcribe", command=self.process_video)
        self.transcribe_button.grid(row=0, column=0, padx=5, pady=5)
        self.process_button = ttk.Button(buttons_frame, text="Transcribe Video", command=self.process_video)
        self.process_button.grid(row=0, column=1, padx=5, pady=5)
        save_transcript_button = ttk.Button(buttons_frame, text="Save Transcript", command=self.save_transcript)
        save_transcript_button.grid(row=0, column=2, padx=5, pady=5)
        clear_button = ttk.Button(buttons_frame, text="Clear", command=self.clear_all)
        clear_button.grid(row=0, column=3, padx=5, pady=5)
        exit_button = ttk.Button(buttons_frame, text="Exit", command=self.root.destroy)
        exit_button.grid(row=0, column=4, padx=5, pady=5)

    def browse_file(self):
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"),
            ("All files", "*.*"),
        ]
        file_path = filedialog.askopenfilename(title="Select a video file", filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)

    def process_video(self):
            video_path = self.file_path_var.get()
            if not video_path:
                messagebox.showwarning("Warning", "Please select a video file first.")
                return
            if not os.path.exists(video_path):
                messagebox.showerror("Error", "The selected file does not exist.")
                return
            if self.is_processing:
                messagebox.showinfo("Processing", "A transcription is already in progress. Please wait.")
                return
            self.is_processing = True
            self.process_button.config(state=tk.DISABLED)
            self.transcribe_button.config(state=tk.DISABLED)
            self.status_var.set("Processing video...")
            self.transcript_text.delete("1.0", tk.END)
            self.processed_text.delete("1.0", tk.END)
            self.progress_var.set(0)
            self.current_task = threading.Thread(target=self.run_transcription, args=(video_path,), daemon=True)
            self.current_task.start()            

    def run_transcription(self, video_path):
            try:
                start_time = time.strftime("%H:%M:%S")  # Record transcription start time
                self.update_status("Converting video to audio...", 10)
                audio_path = self.extract_audio(video_path)
                if not audio_path:
                    raise Exception("Failed to extract audio from video.")
                self.update_status("Transcribing audio...", 30)
                transcript = self.transcribe_audio(audio_path)
                if not transcript:
                    raise Exception("Failed to transcribe audio.")
                end_time = time.strftime("%H:%M:%S")  # Record transcription end time
                self.update_status("Displaying results...", 90)
                self.display_transcript(transcript, start_time, end_time)
                self.update_status("Transcription Complete.", 100)
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as e:
                error_message = str(e)
                self.log_error(f"Transcription failed: {error_message}", include_traceback=True)
                messagebox.showerror("Error", error_message)
                self.update_status("Failed: " + error_message, 0)
            finally:
                self.is_processing = False
                self.process_button.config(state=tk.NORMAL)
                self.transcribe_button.config(state=tk.NORMAL)

    def extract_audio(self, video_path):
            try:
                temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                temp_audio.close()
                audio = AudioSegment.from_file(video_path, format="mp4")
                audio.export(temp_audio.name, format="mp3")
            except Exception as e:
                print(f"No audio found in {video_path}: {e}")
                return None
            return temp_audio.name
    

    def transcribe_audio(self, file_path):
        """
        Sends the local audio file to OpenAI's Whisper API for transcription
        and returns the transcription result (as a dict). The verbose_json format
        includes segments with timestamps.
        """
        self.log_error("Starting transcription with OpenAI...", include_traceback=False)
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}"
        }
        data = {
            "model": "whisper-1",
            "response_format": "verbose_json"  # Request a response that includes timestamps
        }
        try:
            with open(file_path, "rb") as audio_file:
                files = {"file": audio_file}
                response = requests.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()
            self.log_error("Transcription completed successfully.", include_traceback=False)
            result = response.json()
            self.log_error(f"Transcription result: {result}", include_traceback=False)
            return result  # Expecting a dict that includes 'text' and 'segments'
        except Exception as e:
            self.log_error(f"Error transcribing audio with OpenAI: {e}", include_traceback=True)
            return None
