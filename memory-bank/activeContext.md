# Active Context

## Current Focus
- The PyQt5 GUI (`extract_keyframes_gui.py`) is now the only maintained interface, fully replacing the previous Tkinter GUI. Key features include:
  - Video selection (supports full-window drag & drop)
  - Automatic output folder naming
  - Parameter adjustment (sliders, defaults match previous version)
  - Auto-save/reset of parameters
  - Progress bar and percentage display
  - Status display
  - Multithreaded processing
  - Automatically open merged image after completion
  - Auto read/write of config file
  - Modernized UI (fully English, PyQt5-based)

## Virtual Environment Policy
- **Always check if the virtual environment (venv) is activated before running the project.**
  - If not in venv, run: `source venv/bin/activate`
  - If already in venv, run: `python extract_keyframes_gui.py`
  - Do not run both commands together; determine based on current shell state.
- All dependencies (including PyQt5) must be installed in venv to avoid polluting the global environment. requirements.txt is kept in sync and includes PyQt5.

## Next Steps
- For new features or fixes, always check if venv is activated first.
- For new dependencies, always `source venv/bin/activate` before `pip install`.
- Keep activeContext.md, progress.md, and techContext.md updated and in sync.

## Patterns & Preferences
- GUI parameter defaults must match the previous version.
- All user prompts and UI text must be in English.
- Full-window drag & drop is supported for better UX.
- All run/build scripts must check venv status.
- GUI is now fully based on PyQt5; follow techContext.md for dependency installation and development.

## Insights
- Strict virtualenv policy is enforced to avoid ModuleNotFoundError.
- The PyQt5 GUI has fully replaced the old version, providing improved usability and a modern experience.
