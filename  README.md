Here's the complete content for your `README.md` file in a clean, copy-paste ready Markdown format:

# Video Transcription Tool

A Python-based desktop application that transcribes video files using OpenAI's Whisper API, with a user-friendly GUI built using Tkinter.

## Features

- **Video File Selection:** Easily browse and select video files (e.g., MP4, AVI, MOV) for transcription.
- **Transcription Options:** Toggle options such as speaker diarization, auto highlights, and text formatting.
- **Dual Display:** View both the full transcript (with timestamps) and the processed text (raw output) in separate tabs.
- **Audio Extraction:** Automatically extracts audio from video files before sending them to the API.
- **Desktop Shortcut (Windows Only):** Automatically creates a desktop shortcut for quick access.
- **Dependency Check:** Automatically detects and prompts for missing Python packages.

## Prerequisites

- **Python 3.x**
- **Tkinter:** Comes bundled with most Python distributions.
  - On Linux, install via:  
    ```bash
    sudo apt-get install python3-tk
    ```
- **Required Python Packages:**
  - `requests`
  - `pydub`
  - `moviepy`

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourUsername/Video-text-python-tkinter.git
   cd Video-text-python-tkinter
   ```

2. **Install Dependencies:**

   The application automatically checks for missing packages and prompts you to install them. Alternatively, install manually using pip:

   ```bash
   pip install requests pydub moviepy
   ```

3. **Set Up Your OpenAI API Key:**

   Open the source file (`VideoProcessorApp.py`) and locate this line:

   ```python
   self.openai_api_key = "open_api_key"
   ```

   Replace `"open_api_key"` with your actual OpenAI API key.  
   **Recommendation:** For security, load your key from an environment variable instead of hardcoding it.

## Usage

1. **Run the Application:**

   ```bash
   python3 VideoProcessorApp.py
   ```

2. **Using the GUI:**

   - **Select Video:** Click the **"Browse"** button to select your video file.
   - **Transcription Options:** Select your preferences (Speaker Diarization, Auto Highlights, Format Text).
   - **Transcribe:** Click the **"Transcribe"** or **"Transcribe Video"** button to start transcription.
   - **View Results:** The transcript (with timestamps) and processed text (raw output) are displayed in separate tabs.
   - **Save Transcript:** Click **"Save Transcript"** to save your transcript as a `.txt` file.
   - **Clear or Exit:** Use the provided buttons to clear fields or exit the application.

3. **Desktop Shortcut (Windows Only):**

   On Windows, the application attempts to create a desktop shortcut automatically. Ensure `winshell` and `pywin32` are installed if you encounter issues:

   ```bash
   pip install winshell pywin32
   ```

## Troubleshooting

- **Missing Dependencies:**  
  The app will notify you of missing packages and prompt for automatic installation.

- **Tkinter Issues:**  
  On Linux, verify installation of Tkinter:

  ```bash
  sudo apt-get install python3-tk
  ```

- **API Key Concerns:**  
  Always use environment variables or external files (like `.env`) to manage your OpenAI API keys securely. Avoid committing sensitive keys into your codebase.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Open an issue or submit a pull request for any improvements, bug fixes, or new features.
```