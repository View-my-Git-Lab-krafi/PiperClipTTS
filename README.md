# PiperClipTTS

PiperClipTTS is a Python-based tool that monitors the system clipboard for new text and automatically converts it to speech using a Text-to-Speech (TTS) model from Piper. The tool allows users to select different voice models, adjust speech speed, and provides a simple graphical user interface (GUI) to manage the process.

## Features

- **Clipboard Monitoring**: Continuously monitors clipboard for changes and triggers TTS conversion when new text is detected.
- **Model Selection**: Supports multiple TTS voice models, which can be selected via a dropdown menu in the GUI.
- **Adjustable Speech Speed**: Users can modify the speed of the generated speech using a slider control.
- **Audio Playback**: Automatically plays the generated audio after processing.
- **Cross-platform**: Designed to work on Linux, macOS (using `aplay`), and Windows.

## Requirements

- Python 3.x
- Dependencies:
  - `pyperclip`: Clipboard monitoring.
  - `tkinter`: GUI library.
  - `subprocess`: Running external commands.
  - `sox`: Speed adjustment for audio playback (required).
  - Piper TTS models and CLI.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krafi/pipercliptts.git
   cd pipercliptts
   ```

2. **Install Python dependencies**:
   ```bash
   pip install pyperclip
   ```

3. **Install `sox`**:
   - **Linux/macOS**: 
     ```bash
     sudo apt-get install sox
     ```
   - **Windows**: Download and install from [SoX download page](http://sox.sourceforge.net/).

4. **Download Piper TTS models** and place them in the `./onnx/` directory. For example:
   - `ru_RU-denis-medium.onnx`
   - `en_US-bryce-medium.onnx`

## Usage

1. Run the Python script:
   ```bash
   python pipercliptts.py
   ```

2. The GUI will open, allowing you to select a voice model and adjust the speech speed.

3. Once you start monitoring, the program will detect any new text copied to the clipboard and convert it to speech using the selected TTS model.

## Configuration

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

## Controls

- **Model Selection**: Choose the TTS model from the dropdown menu.
- **Speed Adjustment**: Set the desired speech speed using the slider.
- **Start Monitoring**: Click the "Start Monitoring" button to begin clipboard monitoring.

## Known Issues

- Ensure `sox` is installed and available in the system path for proper speed adjustment.
- The program currently supports Linux, macOS, and Windows. Playback uses `aplay` on Linux/macOS and `startfile` on Windows.

## License

This project is open-source under the MIT License. Feel free to contribute and modify!

---

Feel free to modify this README according to your project structure or additional features!
