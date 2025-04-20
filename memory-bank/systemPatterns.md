# System Patterns – Keyframe Extractor

## System Architecture
- Single Python application, with both CLI and GUI entry points
- GUI is based on PyQt5, calling the core logic in extract_keyframes.py
- Video processing and image merging logic are centralized in extract_keyframes.py
- Packaging process is based on py2app, with entry point defined in setup.py

## Key Technical Decisions
- Use OpenCV for video processing and frame difference detection
- Pillow is responsible for image merging and text annotation
- Numpy accelerates image computation
- GUI uses PyQt5 for a modern, cross-platform interface
- macOS packaging uses py2app, with explicit documentation of pyenv dependencies

## Design Patterns in Use
- Shallow MVC separation: GUI (View/Controller) and video processing (Model/Logic) are separated
- Multithreading (threading) to prevent GUI freezing
- Default parameters and user-adjustable options (e.g., diff_threshold, sample_rate)

## Component Relationships
- extract_keyframes_gui.py: Main GUI program, responsible for user interaction and status display
- extract_keyframes.py: Core logic, responsible for video analysis and image merging
- setup.py: Packaging configuration
- requirements.txt: Dependency management
- README.md: Documentation and FAQ

## Critical Implementation Paths
- User operates GUI → selects video/folder → clicks start → runs extract_keyframes → merges images → displays completion/error
- Packaging process: pyenv compiles Python → venv installs dependencies → py2app packages → FAQ troubleshooting
