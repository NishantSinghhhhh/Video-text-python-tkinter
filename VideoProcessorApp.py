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

