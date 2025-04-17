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
