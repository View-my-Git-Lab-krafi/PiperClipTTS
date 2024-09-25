import pyperclip
import time
import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk

class ClipboardMonitor:
    def __init__(self):
        self.models = {
            "ru_RU-denis": "./onnx/ru_RU-denis-medium.onnx",
            "en_US-bryce": "./onnx/en_US-bryce-medium.onnx",
            "ru_RU-irina": "./onnx/ru_RU-irina-medium.onnx",
            "ru_RU-ruslan": "./onnx/ru_RU-ruslan-medium.onnx"
        }
        
        self.model_path = self.models["ru_RU-denis"]
        self.speed = 1.0
        self.last_copied = pyperclip.paste()
        self.audio_process = None
        
        self.output_dir = "./output"
        os.makedirs(self.output_dir, exist_ok=True)  
        
        self.setup_gui()

    def setup_gui(self):
        """Set up the Tkinter GUI."""
        self.root = tk.Tk()
        self.root.title("PiperClipTTS")

        model_label = tk.Label(self.root, text="Select TTS Model:", font=("Helvetica", 14))
        model_label.grid(row=0, column=0, padx=10, pady=5)

        self.model_var = tk.StringVar(value="ru_RU-denis")
        model_dropdown = ttk.Combobox(self.root, textvariable=self.model_var, values=list(self.models.keys()), state="readonly")
        model_dropdown.grid(row=0, column=1, padx=10, pady=5)

        speed_label = tk.Label(self.root, text="Set Speed (0.1 - 2.1):", font=("Helvetica", 14))
        speed_label.grid(row=1, column=0, padx=10, pady=5)

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_slider = tk.Scale(
            self.root, from_=0.1, to=2.1, orient="horizontal", resolution=0.1,
            variable=self.speed_var, length=400,  
            sliderlength=30, 
            font=("Helvetica", 12),  
            tickinterval=0.5 
        )
        speed_slider.grid(row=1, column=1, padx=10, pady=5)

        start_button = tk.Button(self.root, text="Start Monitoring", font=("Helvetica", 14), command=self.start_monitoring)
        start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        self.root.mainloop()

    def start_monitoring(self):
        self.model_path = self.models[self.model_var.get()]
        self.speed = self.speed_var.get()

        threading.Thread(target=self.monitor_clipboard, daemon=True).start()

    def text_to_speech(self, text):
        temp_text_file = os.path.join(self.output_dir, "temp_copyed.txt")
        with open(temp_text_file, "w", encoding="utf-8") as f:
            f.write(text)

        tts_command = f"cat {temp_text_file} | piper --model {self.model_path} --output_file {os.path.join(self.output_dir, 'start.wav')}"
        try:
            print(f"Running TTS command: {tts_command}")
            result = subprocess.run(tts_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("TTS audio generated successfully.")
                self.adjust_speed_and_play(os.path.join(self.output_dir, "start.wav"))
            else:
                print(f"Error running TTS command: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error during TTS process: {e}")

    def adjust_speed_and_play(self, audio_file):
        adjusted_audio_file = os.path.join(self.output_dir, "adjusted_start.wav")
        sox_command = f"sox {audio_file} {adjusted_audio_file} speed {self.speed}"

        try:
            print(f"Adjusting audio speed with sox: {sox_command}")
            subprocess.run(sox_command, shell=True, check=True)
            print(f"Playing audio with speed {self.speed}.")
            self.play_audio(adjusted_audio_file)
        except subprocess.CalledProcessError as e:
            print(f"Error adjusting audio speed: {e}")

    def stop_audio(self):
        """Stop any ongoing audio playback."""
        if self.audio_process and self.audio_process.poll() is None:  # Check if the audio is still playing
            print("Stopping current audio playback.")
            self.audio_process.terminate() 
            self.audio_process = None

    def play_audio(self, audio_file):
        """Play audio file using aplay (Linux/macOS) or startfile (Windows)."""
        self.stop_audio()  # Ensure any ongoing audio is stopped before playing new audio

        if os.name == "posix":  # Linux or macOS
            try:
                print(f"Playing audio: {audio_file}")
                self.audio_process = subprocess.Popen(["aplay", audio_file])
            except Exception as e:
                print(f"Error playing audio: {e}")
        elif os.name == "nt":  # Windows
            try:
                print(f"Playing audio: {audio_file}")
                self.audio_process = subprocess.Popen(["start", audio_file], shell=True)
            except Exception as e:
                print(f"Error playing audio: {e}")

    def monitor_clipboard(self):
        """Monitor the clipboard for changes and generate speech for new text."""
        while True:
            current_copied = pyperclip.paste()
            if current_copied != self.last_copied:
                print("Something new has been copied to the clipboard!")
                print(f"Copied text: {current_copied}")
                self.last_copied = current_copied

                self.stop_audio()

                tts_thread = threading.Thread(target=self.text_to_speech, args=(current_copied,))
                tts_thread.start()

            time.sleep(0.5)

if __name__ == "__main__":
    monitor = ClipboardMonitor()

