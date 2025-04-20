# Tech Context – Keyframe Extractor

## Technologies Used
- Python 3.12+ (recommended to build with pyenv)
- OpenCV (cv2): video processing
- Pillow (PIL): image merging and annotation
- Numpy: image computation
- PyQt5: GUI
- py2app: macOS packaging
- pyenv, venv: Python environment management

## Development Setup
- It is recommended to use Homebrew to install pyenv
- Build Python with pyenv; PyQt5 must be installed in venv
- Use venv to create an isolated environment and install dependencies from requirements.txt
- For development, run `extract_keyframes_gui.py` to launch the PyQt5 GUI

## Technical Constraints
- macOS packaging is supported via py2app; Windows/Linux packaging requires separate planning
- Dependencies must be clearly listed in requirements.txt
- GUI is based solely on PyQt5, providing a modern interface and improved interactivity

## Dependencies
- Managed via requirements.txt
- Main dependencies: opencv-python, pillow, numpy, PyQt5

## Tool Usage Patterns
- Both CLI and GUI are available; GUI is based on PyQt5
- Packaging process is detailed in README.md
- FAQ and troubleshooting are included in the documentation
