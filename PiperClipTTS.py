import pyperclip
import time
import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk
import argostranslate.package
import argostranslate.translate
import re
class ClipboardMonitor:
    def __init__(self):
        self.models = {
            "ru_RU-denis": "./onnx/ru_RU-denis-medium.onnx",
            "en_US-bryce": "./onnx/en_US-bryce-medium.onnx",
            "ru_RU-irina": "./onnx/ru_RU-irina-medium.onnx",
            "ru_RU-ruslan": "./onnx/ru_RU-ruslan-medium.onnx"
        }
        print("If you want more language model. Visit:-")
        print("https://rhasspy.github.io/piper-samples/")
        print("https://github.com/rhasspy/piper/blob/master/VOICES.md")
        self.model_path = self.models["ru_RU-denis"]
        self.speed = 1.0
        self.last_copied = pyperclip.paste()
        self.audio_process = None
        

        self.languages = {
            "Russian": "ru",
            "English": "en",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Albanian": "sq",
            "Arabic": "ar",
            "Azerbaijani": "az",
            "Bengali": "bn",
            "Bulgarian": "bg",
            "Catalan": "ca",
            "Chinese (traditional)": "zt",
            "Chinese": "zh",
            "Czech": "cs",
            "Danish": "da",
            "Dutch": "nl",
            "Esperanto": "eo",
            "Estonian": "et",
            "Finnish": "fi",
            "Greek": "el",
            "Hebrew": "he",
            "Hindi": "hi",
            "Hungarian": "hu",
            "Indonesian": "id",
            "Irish": "ga",
            "Italian": "it",
            "Japanese": "ja",
            "Korean": "ko",
            "Latvian": "lv",
            "Lithuanian": "lt",
            "Malay": "ms",
            "Norwegian": "nb",
            "Persian": "fa",
            "Polish": "pl",
            "Portuguese": "pt",
            "Romanian": "ro",
            "Slovak": "sk",
            "Slovenian": "sl",
            "Tagalog": "tl",
            "Thai": "th",
            "Turkish": "tr",
            "Ukrainian": "uk",
            "Urdu": "ur"
        }

        self.output_dir = "./output"
        os.makedirs(self.output_dir, exist_ok=True)

        self.from_code = "ru"
        self.to_code = "en"

        self.sentence_mode = False
        
        self.translate_enabled = True
        self.translated_model_path = self.models["en_US-bryce"]
        self.setup_gui()
            
        '''
        
        # Translation enable/disable checkbox
        translate_label = tk.Label(self.root, text="Enable Translation:", font=("Helvetica", 14))
        translate_label.grid(row=9, column=0, padx=10, pady=5)

        self.translate_var = tk.BooleanVar(value=True)
        translate_checkbox = tk.Checkbutton(self.root, text="Enable Translation", variable=self.translate_var)
        translate_checkbox.grid(row=9, column=1, padx=10, pady=5)
        '''
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("PiperClipTTS")
        self.translate_var = tk.BooleanVar(value=True)
        # Model selection
        model_label = tk.Label(self.root, text="Select TTS Model:", font=("Helvetica", 14))
        model_label.grid(row=0, column=0, padx=10, pady=5)

        self.model_var = tk.StringVar(value="ru_RU-denis")
        model_dropdown = ttk.Combobox(self.root, textvariable=self.model_var, values=list(self.models.keys()), state="readonly")
        model_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Speed selection
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

        # Translate and TTS option
        translate_tts_label = tk.Label(self.root, text="Translate and Read:", font=("Helvetica", 14))
        translate_tts_label.grid(row=2, column=0, padx=10, pady=5)

        self.translate_tts_var = tk.BooleanVar(value=False)
        translate_tts_checkbox = tk.Checkbutton(self.root, text="Translate and Read", variable=self.translate_tts_var, command=self.toggle_translation_options)
        translate_tts_checkbox.grid(row=2, column=1, padx=10, pady=5)

        # Language selection for translation (from language)
        from_language_label = tk.Label(self.root, text="Same as TTS Model:", font=("Helvetica", 14))
        from_language_label.grid(row=3, column=0, padx=10, pady=5)

        self.from_language_var = tk.StringVar(value="Russian")
        from_language_dropdown = ttk.Combobox(self.root, textvariable=self.from_language_var, values=list(self.languages.keys()), state="readonly")
        from_language_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Language selection for translation (to language)
        to_language_label = tk.Label(self.root, text="Translation To: ", font=("Helvetica", 14))
        to_language_label.grid(row=4, column=0, padx=10, pady=5)

        self.to_language_var = tk.StringVar(value="English")
        to_language_dropdown = ttk.Combobox(self.root, textvariable=self.to_language_var, values=list(self.languages.keys()), state="readonly")
        to_language_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Mode selection (sentence-by-sentence or full-text)
        mode_label = tk.Label(self.root, text="Play Mode:", font=("Helvetica", 14))
        mode_label.grid(row=5, column=0, padx=10, pady=5)

        self.sentence_mode_var = tk.BooleanVar(value=False)
        mode_checkbox = tk.Checkbutton(self.root, text="Sentence by Sentence", variable=self.sentence_mode_var)
        mode_checkbox.grid(row=5, column=1, padx=10, pady=5)

        # TTS model selection for translated text
        translated_model_label = tk.Label(self.root, text="Select TTS Model for Translated Text:", font=("Helvetica", 14))
        translated_model_label.grid(row=6, column=0, padx=10, pady=5)

        self.translated_model_var = tk.StringVar(value="en_US-bryce")
        translated_model_dropdown = ttk.Combobox(self.root, textvariable=self.translated_model_var, values=list(self.models.keys()), state="readonly")
        translated_model_dropdown.grid(row=6, column=1, padx=10, pady=5)

        # Instructional label
        instruction_label = tk.Label(
            self.root,
            text="For the first use of the Translate feature, please wait a few minutes after listening to the TTS voice for your selected language translation library to download.",
            font=("Helvetica", 12),
            wraplength=800, 
            justify="center"
        )
        instruction_label.grid(row=7, column=0, columnspan=2, padx=35, pady=15, sticky="nsew")

        start_button = tk.Button(self.root, text="Start Monitoring", font=("Helvetica", 14), command=self.start_monitoring)
        start_button.grid(row=8, column=0, columnspan=2, padx=10, pady=20)

        self.translation_widgets = [
            from_language_label, from_language_dropdown,
            to_language_label, to_language_dropdown,
            mode_label, mode_checkbox,
            translated_model_label, translated_model_dropdown,
            instruction_label
        ]

        # Initially toggle based on the default state of the checkbox
        self.toggle_translation_options()

        self.root.mainloop()

    def toggle_translation_options(self):
        if self.translate_tts_var.get():
            for widget in self.translation_widgets:
                widget.grid()
        else:
            for widget in self.translation_widgets:
                widget.grid_remove()



    def update_translation_languages(self):
        self.from_code = self.languages[self.from_language_var.get()]
        self.to_code = self.languages[self.to_language_var.get()]
        print(f"Translation languages updated: {self.from_code} to {self.to_code}")
        self.install_translation_package()

    def install_translation_package(self):
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()

        try:
            package_to_install = next(
                filter(
                    lambda x: x.from_code == self.from_code and x.to_code == self.to_code,
                    available_packages,
                )
            )
            print("\033[91mDownloading ..... Please wait.../\033[0m")
            argostranslate.package.install_from_path(package_to_install.download())
        except StopIteration:
            print("\033[91mNo suitable translation package found. Please visit this website to check supported languages: https://www.argosopentech.com/argospm/index/\033[0m")

    def translate_text(self, text):
        translated_text = argostranslate.translate.translate(text, self.from_code, self.to_code)
        print(f"Translated text: {translated_text}")
        return translated_text

    def start_monitoring(self):
        self.model_path = self.models[self.model_var.get()]
        self.translated_model_path = self.models[self.translated_model_var.get()]
        self.speed = self.speed_var.get()

        self.update_translation_languages()

        self.translate_enabled = self.translate_var.get()
        self.sentence_mode = self.sentence_mode_var.get()

        self.translate_tts_enabled = self.translate_tts_var.get()  # Get the new checkbox value

        threading.Thread(target=self.monitor_clipboard, daemon=True).start()


    def split_sentences(self, text):
        sentence_endings = r'[.!?]+'
        sentences = re.split(sentence_endings, text)
        sentences = [s.strip() + '.' for s in sentences if s.strip()]
        return sentences


    def text_to_speech(self, text, translated=False):
        filename_suffix = "translated" if translated else "original"
        temp_text_file = os.path.join(self.output_dir, f"temp_{filename_suffix}.txt")
        with open(temp_text_file, "w", encoding="utf-8") as f:
            f.write(text)

        # Use the selected TTS model for the translated text
        if translated:
            model_path = self.translated_model_path
        else:
            model_path = self.model_path

        tts_command = f"cat {temp_text_file} | piper --model {model_path} --output_file {os.path.join(self.output_dir, f'{filename_suffix}.wav')}"
        try:
            print(f"Running TTS command: {tts_command}")
            result = subprocess.run(tts_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"TTS audio generated successfully for {filename_suffix}.")
                self.adjust_speed_and_play(os.path.join(self.output_dir, f"{filename_suffix}.wav"), translated)
            else:
                print(f"Error running TTS command for {filename_suffix}: {result.stderr}")
        except subprocess.CalledProcessError as e:
            print(f"Error during TTS process: {e}")

    def adjust_speed_and_play(self, audio_file, translated=False):
        """Adjust the audio speed and play it."""
        adjusted_audio_file = os.path.join(self.output_dir, f"adjusted_{'translated' if translated else 'original'}.wav")
        sox_command = f"sox {audio_file} {adjusted_audio_file} speed {self.speed}"

        try:
            print(f"Adjusting audio speed with sox: {sox_command}")
            subprocess.run(sox_command, shell=True, check=True)
            print(f"Playing audio with speed {self.speed}.")
            self.play_audio(adjusted_audio_file, translated)
        except subprocess.CalledProcessError as e:
            print(f"Error adjusting audio speed: {e}")

    def stop_audio(self):
        """Stop any ongoing audio playback."""
        if self.audio_process and self.audio_process.poll() is None:
            print("Stopping current audio playback.")
            self.audio_process.terminate()
            self.audio_process = None

    def play_audio(self, audio_file, translated=False):
        """Play the audio file using appropriate command depending on OS."""
        self.stop_audio() 
        if os.name == "posix":  # Linux/macOS
            try:
                print(f"Playing audio: {audio_file}")
                self.audio_process = subprocess.Popen(["aplay", audio_file])
                self.audio_process.wait() 
            except Exception as e:
                print(f"Error playing audio: {e}")
        elif os.name == "nt":  # Windows
            try:
                print(f"Playing audio: {audio_file}")
                self.audio_process = subprocess.Popen(["start", audio_file], shell=True)
                self.audio_process.wait()  # Wait for the process to finish
            except Exception as e:
                print(f"Error playing audio: {e}")

        if translated:
            print("Translation audio completed.")

    def monitor_clipboard(self):
        while True:
            current_copied = pyperclip.paste()
            if current_copied != self.last_copied:
                print("Something new has been copied to the clipboard!")
                print(f"Copied text: {current_copied}")
                self.last_copied = current_copied
                self.stop_audio()
                if self.sentence_mode:
                    sentences = self.split_sentences(current_copied)
                    for sentence in sentences:
                        # Read original text
                        tts_thread = threading.Thread(target=self.text_to_speech, args=(sentence,))
                        tts_thread.start()
                        tts_thread.join()
                        # Check if translation is enabled and "Translate and Read" is checked
                        if self.translate_enabled and self.translate_tts_enabled:
                            translated_text = self.translate_text(sentence)
                            translated_tts_thread = threading.Thread(target=self.text_to_speech, args=(translated_text, True))
                            translated_tts_thread.start()
                            translated_tts_thread.join()
                else:
                    # Read original text
                    tts_thread = threading.Thread(target=self.text_to_speech, args=(current_copied,))
                    tts_thread.start()
                    tts_thread.join()
                    # Check if translation is enabled and "Translate and Read" is checked
                    if self.translate_enabled and self.translate_tts_enabled:
                        translated_text = self.translate_text(current_copied)
                        translated_tts_thread = threading.Thread(target=self.text_to_speech, args=(translated_text, True))
                        translated_tts_thread.start()
                        translated_tts_thread.join()
            time.sleep(0.5)


if __name__ == "__main__":
    monitor = ClipboardMonitor()

