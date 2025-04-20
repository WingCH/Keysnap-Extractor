# Tech Context – Keyframe Extractor

## Technologies Used
- Python 3.12 (recommended to build with pyenv, supports tcl-tk@8)
- OpenCV (cv2): video processing
- Pillow (PIL): image merging and annotation
- Numpy: image computation
- tkinter: GUI
- py2app: macOS packaging
- pyenv, venv: Python environment management

## Development Setup
- It is recommended to use Homebrew to install pyenv and tcl-tk@8
- Build Python with pyenv to ensure tkinter support
- Use venv to create an isolated environment and install dependencies from requirements.txt
- For development, you can directly run extract_keyframes_gui.py to test the GUI

## Technical Constraints
- macOS packaging requires correct linking to tcl-tk@8, otherwise tkinter will be missing
- py2app only supports macOS; Windows/Linux packaging requires separate planning
- Dependencies must be clearly listed in requirements.txt
- GUI is based on tkinter, which is limited in appearance but cross-platform

## Dependencies
- Managed via requirements.txt
- Main dependencies: opencv-python, pillow, numpy

## Tool Usage Patterns
- Both CLI and GUI are available, with GUI based on tkinter
- Packaging process is detailed in README.md
- FAQ and troubleshooting are included in the documentation
