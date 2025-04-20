# Product Context – Keyframe Extractor

## Why does this project exist?
Modern video content is vast, making it difficult to quickly identify key segments. Users (such as educators, creators, and general viewers) often spend a lot of time watching entire videos just to find important parts.  
Keyframe Extractor aims to automate this process, allowing users to obtain the main points of a video with one click, improving information acquisition efficiency.

## Problems it solves
- Saves users' time spent browsing videos
- Automatically detects and extracts "still" or important frames
- Merges all keyframes into a single image for quick viewing and sharing
- Lowers the barrier for beginners, eliminating tedious manual screenshots

## How should it work?
- Users only need to select a video and output folder, then click "Start Extraction"
- The program automatically analyzes the video, extracts keyframes, merges them, and annotates timestamps
- Upon completion, a popup notifies the user, and the merged image can be opened directly

## User experience goals
- Simple and intuitive workflow, no technical background required
- Modern and clear GUI (PyQt5), with clear status feedback
- Instant error prompts and troubleshooting suggestions for common issues
- Complete documentation and FAQ friendly to beginners
- Supports macOS packaging, with future extensibility to Windows/Linux
