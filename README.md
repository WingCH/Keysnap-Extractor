# Keyframe Extractor

## What does this project do?

This project helps you quickly review the main content of a video by automatically extracting keyframes (important screenshots) and combining them into a single image. Instead of watching the whole video, you can see all the important moments at a glance.

## How does it work?

1. The script reads your video file (e.g. `input.mp4`).
2. It checks every frame and compares it to the previous frames.
3. If the video becomes "still" (no big changes for a few frames), it saves that frame as a keyframe.
4. All keyframes are combined into one image, arranged in rows (5 images per row).
5. Each keyframe shows the timestamp at the bottom left, so you know when it happened in the video.

## Technologies used

- **Python 3**
- **OpenCV (cv2)**: For reading video and image processing.
- **Pillow (PIL)**: For image merging and drawing text.
- **Numpy**: For fast image calculations.

## How to use

1. Put your video file as `input.mp4` in the project folder.
2. Make sure you have Python 3 and the required packages installed:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

After activation, your Terminal prompt will show `(venv)` at the front, meaning you are inside the virtual environment.

   ```
   pip install -r requirements.txt
   ```

#### Install packages

With the virtual environment activated, install packages (these will not affect other projects):

```
pip install -r requirements.txt
```

---

## FAQ

### Q1: Why do I get `No module named '_tkinter'` when building or running the app?
A: Your Python was not built with Tcl/Tk support. Please follow the "Build Python with Tcl/Tk support" section and ensure you use the correct Homebrew tcl-tk@8 path.

### Q2: The GUI app does not launch or crashes immediately. What should I check?
A: Make sure you are using the virtual environment created from the correct pyenv Python version (with Tcl/Tk support). Activate the venv before running or building.

### Q3: I get errors about missing modules (e.g. `ModuleNotFoundError`) after building.
A: Double-check that you installed all dependencies inside the venv:  
```
pip install -r requirements.txt
```
Then rebuild the app.

### Q4: Can I build this app on Windows or Linux?
A: The current instructions are for macOS (py2app). For Windows, consider using [pyinstaller](https://pyinstaller.org/) or [cx_Freeze](https://cx-freeze.readthedocs.io/). For Linux, you can run the script directly with Python and the required packages. Cross-platform packaging is not yet documented here.

### Q5: How do I update dependencies?
A: Edit `requirements.txt` and run:
```
pip install -r requirements.txt
```
Rebuild the app if needed.

---

## How to build a standalone macOS app (py2app, tkinter, pyenv)

### 1. Install Homebrew dependencies

You need Homebrew and the following packages:

```sh
brew install pyenv pyenv-virtualenv
brew install tcl-tk@8
```

### 2. Build Python with Tcl/Tk support

macOS system Python or default pyenv Python may not include tkinter.  
You must build Python with explicit tcl-tk@8 support:

```sh
env \
  LDFLAGS="-L/opt/homebrew/opt/tcl-tk@8/lib" \
  CPPFLAGS="-I/opt/homebrew/opt/tcl-tk@8/include" \
  PKG_CONFIG_PATH="/opt/homebrew/opt/tcl-tk@8/lib/pkgconfig" \
  pyenv install 3.12.3
```

### 3. Create and activate a virtual environment

```sh
pyenv shell 3.12.3
python -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```sh
pip install -r requirements.txt
```

### 5. Build the app with py2app

```sh
python setup.py py2app
```

The built app will be in `dist/extract_keyframes_gui.app`.

### 6. Run the app

```sh
open dist/extract_keyframes_gui.app
```

### Troubleshooting

- **No module named '_tkinter'**:  
  Your Python was not built with Tcl/Tk support.  
  Make sure you followed step 2 and used the correct Homebrew tcl-tk@8 path.

- **GUI does not launch or crashes**:  
  Ensure you are using the venv created from the correct pyenv Python version.

- **Other missing modules**:  
  Double-check `requirements.txt` and re-run `pip install -r requirements.txt` in your venv.

---
