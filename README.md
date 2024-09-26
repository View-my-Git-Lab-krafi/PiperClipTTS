
# PiperClipTTS

PiperClipTTS is a Python-based tool that monitors the system clipboard for new text and automatically converts it to speech using a Text-to-Speech (TTS) model from Piper. The tool also provides a translation feature, allowing clipboard text to be translated and spoken in different languages. A simple graphical user interface (GUI) allows users to manage the process with ease.

## Features

- **Clipboard Monitoring**: Continuously monitors clipboard for changes and triggers TTS conversion when new text is detected.
- **Model Selection**: Supports multiple TTS voice models, selectable via a dropdown menu in the GUI.
- **Adjustable Speech Speed**: Users can modify the speed of the generated speech using a slider control.
- **Audio Playback**: Automatically plays the generated audio after processing.
- **Translation**: Automatically translates clipboard text into another language and converts it to speech. Supports many languages via Argos Translate.
- **Sentence Mode**: Option to play text sentence-by-sentence, translating and speaking each sentence individually.
- **Cross-platform**: Designed to work on Linux, macOS (using `aplay`), and Windows.

## Requirements

- Python 3.x
  - Recommend Python 3.10 (there may be issues with other versions).
- Dependencies:
  - `pyperclip`: Clipboard monitoring.
  - `tkinter`: GUI library.
  - `subprocess`: Running external commands.
  - `sox`: Speed adjustment for audio playback (required).
  - `argostranslate`: Translation support.
  - Piper TTS models and CLI.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krafi/pipercliptts.git
   cd pipercliptts
   ```

2. **Install Python dependencies**:
   ```bash
   pip install pyperclip argostranslate
   ```
3. **Install Python dependencies using requirements.txt:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Install `sox`**:
   - **Linux/macOS**: 
     ```bash
     sudo apt-get install sox
     ```
   - **Windows**: Download and install from [SoX download page](http://sox.sourceforge.net/).


## Usage

1. Run the Python script:
   ```bash
   python pipercliptts.py
   ```

2. The GUI will open, allowing you to select a voice model, translation languages, and adjust the speech speed.

3. Once you start monitoring, the program will detect any new text copied to the clipboard, First speech that text then translate it (if selected), and convert it to speech according to your language.

## Configuration
 **Download Piper TTS models** and place them in the `./onnx/` directory. For example: (Optional)
   - `ru_RU-denis-medium.onnx`
   - `en_US-bryce-medium.onnx`
   You can find on 
   [https://github.com/rhasspy/piper/blob/master/VOICES.md](https://github.com/rhasspy/piper/blob/master/VOICES.md)
   [https://rhasspy.github.io/piper-samples/](https://rhasspy.github.io/piper-samples/)
- **Models**: Modify or add new models by updating the `models` dictionary in the script:
  ```python
  self.models = {
      "ru_RU-denis": "./onnx/ru_RU-denis-medium.onnx",
      "en_US-bryce": "./onnx/en_US-bryce-medium.onnx",
      "ru_RU-irina": "./onnx/ru_RU-irina-medium.onnx",
      "ru_RU-ruslan": "./onnx/ru_RU-ruslan-medium.onnx"
  }
  ```

- **Speed Adjustment**: Control speech speed using the slider, with a range of `0.1` to `2.1` (default is `1.0`).

- **Translation**: You can translate the clipboard text from one language to another. The supported languages are listed in the GUI and include Russian, English, French, Spanish, German, Chinese, Arabic, and many others.

## Controls

- **Model Selection**: Choose the TTS model from the dropdown menu.
- **Speed Adjustment**: Set the desired speech speed using the slider.
- **Translation Settings**: Select the source and target languages for translation.
- **Sentence Mode**: Toggle sentence-by-sentence playback and translation.
- **Start Monitoring**: Click the "Start Monitoring" button to begin clipboard monitoring.

## Known Issues

- Ensure `sox` is installed and available in the system path for proper speed adjustment.
- The translation feature may take a few minutes on the first run as it downloads the necessary language packages.
- The program currently supports Linux, macOS, and Windows. Playback uses `aplay` on Linux/macOS and `startfile` on Windows.

## License

This project is open-source under the GPL-3 License. Feel free to contribute and modify!
