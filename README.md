# FStools

### A Lightweight Desktop Application for GUI Automation and Browser Embedding

FStools is a simple desktop application built with **Python + PyQt5**. It's intended as a **personal productivity and educational tool** for experimenting with GUI automation and browser embedding.

---

## Key Features

- **Embedded Browser**: Integrates a browser window directly into the application.
- **Keyboard Automation**: Automates key presses with configurable delays.
- **Sequence Builder**: Create sequences of hotkeys (1-9) for repetitive actions.
- **Background Operation**: Automation continues to run even when the application window is not in focus.
- **Simple Graphical Controller**: Control the automation process with an easy-to-use interface.

---

## Requirements

- **Python 3.10+**

**Python Dependencies:**

- `keyboard`
- `pywin32`
- `PyQt5`
- `PyQtWebEngine`

---

## Installation

1.  **Clone the repository:**
    ```bash
    https://github.com/RahmanYazid/FSTools.git
    cd Flyff-assist
    ```
2.  **Install dependencies:**
    ```bash
    python -m pip install -r requirements.txt
    ```

---

## Usage

1.  **Run the application:**
    ```bash
    python Flyff-FS.py
    ```
    The app will open with an embedded browser window.
2.  **Configure**: Use the **controller** to define your desired hotkey sequence.
3.  **Start**: The automation will press keys `1–9` in your chosen order with a custom delay.

---

**Important Disclaimer**

This project is for **educational and personal use only**. It serves as a generic demonstration of keyboard automation and browser embedding. The author is not affiliated with any game or service, and this tool should not be used to violate any software's Terms of Service (ToS).
