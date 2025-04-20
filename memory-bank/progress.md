# Progress – Keyframe Extractor

## What works
- Automatic extraction of keyframes from videos and merging into a single image is stable
- PyQt5 GUI (`extract_keyframes_gui.py`) is modern, supports drag & drop, parameter adjustment, progress bar, and multithreading
- macOS packaging (py2app) process is complete, FAQ section helps beginners troubleshoot
- Documentation (README.md) is well-structured, memory bank is established and kept in sync

## What's left to build
- Further GUI enhancements (such as image preview, more interactive prompts)
- Windows/Linux packaging instructions and automation scripts (Makefile, shell script)
- More detailed error handling and user prompts
- Regularly update the memory bank to ensure no knowledge is lost

## Current status
- The project is stable and suitable for beginners and general users
- Handover documents and knowledge base (memory bank) are complete, facilitating team collaboration

## Known issues
- Currently, only macOS packaging has complete instructions; Windows/Linux is not yet supported
- Only MP4 video format is supported; other formats need to be added in the future

## Evolution of project decisions
- Initially CLI-focused, later shifted to GUI to improve usability
- GUI is now fully based on PyQt5, replacing the legacy tkinter version
- Packaging process optimized multiple times, finally adopted pyenv + py2app
- FAQ and memory bank incorporated into project standard workflow, improving handover and maintenance efficiency
