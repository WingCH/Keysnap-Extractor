# Keyframe Extractor

Automatically extract keyframes from videos and merge them into a single image, allowing you to grasp the main content of a video at a glance.

https://github.com/user-attachments/assets/b5922cfb-0727-4f04-a174-5b0e1954f4cb

---

## Project Overview

Keyframe Extractor helps users quickly review the highlights of a video, saving time from frame-by-frame viewing. Simply select a video and click "Start Extraction"—the program will analyze, extract keyframes, and merge them into a single image with timestamp annotations. Ideal for educators, creators, and general users.

---

## Features

- Automatically analyze MP4 videos and extract keyframes
- Merge all keyframes into a single image with timestamp annotations
- Modern PyQt5 GUI (supports drag & drop, parameter adjustment, progress bar, multithreading)
- macOS packaging support (py2app)
- Complete installation, packaging, and troubleshooting instructions
- Beginner-friendly: easy to install and use

---

## Tech Stack

- **Python 3.12+**
- **OpenCV (cv2):** Video processing and frame difference detection
- **Pillow (PIL):** Image merging and text annotation
- **Numpy:** Accelerated image computation
- **PyQt5:** Modern GUI
- **py2app:** macOS packaging
- **venv/pyenv:** Virtual environment and Python management

---

## Installation & Getting Started

### 1. Create a virtual environment and install dependencies

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Launch the PyQt5 GUI

```sh
python extract_keyframes_gui.py
```

### 3. CLI Usage (for advanced users)

```sh
python extract_keyframes.py --input input.mp4 --output output_folder/
```

### 4. macOS Packaging (py2app)

1. Install Homebrew dependencies:
    ```sh
    brew install pyenv pyenv-virtualenv
    ```
2. Use pyenv to install Python 3.12+, create a venv, and install dependencies.
3. Build the app:
    ```sh
    python setup.py py2app
    ```
4. The generated app will be in the `dist/` directory and can be opened directly.

---

## Usage Workflow

1. Launch `extract_keyframes_gui.py`
2. Drag and drop a video file into the window or use the file selector
3. Set the output folder and parameters (defaults are available)
4. Click "Start Extraction"
5. The program will analyze, extract, merge, and annotate keyframes automatically
6. The merged image will open automatically upon completion

---

## FAQ

**Q1: I get `ModuleNotFoundError` when running?**  
A: Make sure you have activated the venv and installed all dependencies:  
```sh
source venv/bin/activate
pip install -r requirements.txt
```

**Q2: The GUI does not launch or crashes?**  
A: Ensure you are using Python installed via pyenv, have activated the venv, and installed PyQt5.

**Q3: How do I run this on Windows/Linux?**  
A: Packaging instructions are currently for macOS only. On Windows/Linux, run the script directly with Python and install the required dependencies yourself.

**Q4: How do I update dependencies?**  
A: Edit `requirements.txt` and run:  
```sh
pip install -r requirements.txt
```

---

## Project Status & Roadmap

- PyQt5 GUI has fully replaced the legacy tkinter version, offering a more complete and modern interface
- macOS packaging is supported; Windows/Linux packaging is planned
- Only MP4 format is currently supported; more formats will be added in the future
- Contributions via issues/PRs are welcome

---

## Contributing

1. Fork this repository and create a feature branch
2. Ensure basic tests pass before submitting a PR
3. For significant changes, please update the memory-bank/ documentation as well

---

For more technical details, design patterns, and development context, please refer to the files in the `memory-bank/` directory.
