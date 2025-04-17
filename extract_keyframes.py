import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

VIDEO_PATH = "input.mp4"
OUTPUT_DIR = "keyframes"
MERGED_IMAGE_PATH = "keyframes_merged.png"
FRAME_DIFF_THRESHOLD = 25  # Lower = more sensitive
FRAME_SAMPLE_RATE = 24     # Frames per second to sample, 24=all, 1=one per second
MIN_KEYFRAME_INTERVAL = 0.5  # Minimum seconds between two keyframes

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_frame_diff(img1, img2):
    # Calculate mean pixel difference between two grayscale images
    diff = cv2.absdiff(img1, img2)
    return np.mean(diff)

def extract_keyframes(
    video_path, output_dir, diff_threshold=25, sample_rate=24, min_interval=0.5,
    stillness_threshold=3, stillness_frames=5
):
    """
    Only extract keyframe when the image is stable for stillness_frames frames.
    stillness_threshold: pixel diff threshold to consider as 'still'
    stillness_frames: how many frames must be still to be considered stable
    """
    ensure_dir(output_dir)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps // sample_rate)
    prev_gray = None
    keyframes = []
    frame_idx = 0
    keyframe_idx = 0
    last_keyframe_time = -min_interval
    stillness_queue = []
    prev_state_still = False  # Is currently in still state

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval != 0:
            frame_idx += 1
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        if prev_gray is not None:
            diff = get_frame_diff(prev_gray, gray)
            stillness_queue.append(diff)
            if len(stillness_queue) > stillness_frames:
                stillness_queue.pop(0)
        else:
            stillness_queue.append(0)
        prev_gray = gray

        # Check if current state is still
        is_still = (
            len(stillness_queue) == stillness_frames
            and all(d < stillness_threshold for d in stillness_queue)
        )

        # Only extract keyframe when entering still state from moving state
        if (
            is_still
            and not prev_state_still
            and (timestamp - last_keyframe_time) >= min_interval
        ):
            out_path = os.path.join(output_dir, f"keyframe_{keyframe_idx:03d}_{timestamp:.2f}.png")
            cv2.imwrite(out_path, frame)
            keyframes.append((out_path, timestamp))
            keyframe_idx += 1
            last_keyframe_time = timestamp

        prev_state_still = is_still
        frame_idx += 1
    cap.release()
    return keyframes

def merge_keyframes(keyframes, merged_path, max_per_row=8):
    images = [Image.open(path) for path, _ in keyframes]
    if not images:
        print("No keyframes to merge.")
        return
    w, h = images[0].size
    n = len(images)
    rows = (n + max_per_row - 1) // max_per_row
    cols = min(n, max_per_row)
    merged_img = Image.new("RGB", (cols * w, rows * h), (0, 0, 0))
    try:
        font = ImageFont.truetype("Arial.ttf", 80)
    except Exception as e:
        print("Failed to load Arial.ttf, fallback to default font:", e)
        font = ImageFont.load_default()
    for idx, (img, (_, timestamp)) in enumerate(zip(images, keyframes)):
        row = idx // max_per_row
        col = idx % max_per_row
        x = col * w
        y = row * h
        merged_img.paste(img, (x, y))
        draw = ImageDraw.Draw(merged_img)
        text = f"{timestamp:.2f}s"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        # Add padding, move background and text up to avoid clipping
        padding = 20
        rect_y0 = y + h - text_h - padding * 2
        rect_y1 = y + h
        text_x = x + padding
        text_y = y + h - text_h - padding
        draw.rectangle(
            [x, rect_y0, x + text_w + padding * 2, rect_y1],
            fill=(0, 0, 0, 180)
        )
        draw.text(
            (text_x, text_y),
            text,
            fill=(255, 255, 0),
            font=font
        )
    merged_img.save(merged_path)
    print(f"Merged image saved to {merged_path}")

if __name__ == "__main__":
    keyframes = extract_keyframes(
        VIDEO_PATH, OUTPUT_DIR, FRAME_DIFF_THRESHOLD, FRAME_SAMPLE_RATE, MIN_KEYFRAME_INTERVAL,
        stillness_threshold=3, stillness_frames=5
    )
    merge_keyframes(keyframes, MERGED_IMAGE_PATH, max_per_row=5)
