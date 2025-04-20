# Active Context – Keyframe Extractor

## Current Work Focus
- GUI interface internationalization: all interface text switched from Traditional Chinese to English
- GUI improvements (progress bar, status color, modern color/font, button interaction)
- README.md FAQ expansion for troubleshooting
- Memory bank established and kept in sync

## Recent Changes
- extract_keyframes_gui.py: All interface text translated to English for internationalization
- GUI beautification: ttk.Progressbar, status color, font/color, button hover/active effect
- README.md: Added FAQ section (tkinter, py2app, dependencies, platform issues)
- memory-bank/: projectbrief.md, productContext.md, systemPatterns.md, techContext.md completed

## Next Steps
- Further GUI improvements (image preview, drag-and-drop, more interaction)
- Add Windows/Linux packaging instructions
- Add automation scripts (Makefile, shell script)
- Regularly update memory bank with major decisions and learnings

## Active Decisions & Considerations
- tkinter as main GUI, balancing aesthetics and cross-platform
- Packaging flow prioritizes macOS/py2app, Windows/Linux to be added
- Documentation and FAQ to be kept up-to-date for easier onboarding

## Important Patterns & Preferences
- Clear color distinction for status (blue/green/red)
- Threading to avoid GUI freeze
- Documentation and code kept in sync

## Learnings & Insights
- macOS tkinter/py2app packaging requires special attention to tcl-tk dependencies
- FAQ greatly reduces common beginner issues
- Memory bank is critical for team handoff and knowledge retention
- Internationalization (i18n) is important for broader user base and future localization
