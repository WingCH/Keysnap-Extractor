import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
import subprocess
import json
from extract_keyframes import extract_keyframes, merge_keyframes

VIDEO_EXTENSIONS = [("MP4 files", "*.mp4"), ("All files", "*.*")]
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
MERGED_IMAGE_PATH = "keyframes_merged.png"

def run_extraction(
    video_path, output_dir, status_label, progress, root, open_btn,
    diff_threshold, sample_rate, min_interval, stillness_threshold, stillness_frames
):
    try:
        # Get percent_label
        percent_label = None
        for widget in root.winfo_children():
            if isinstance(widget, tk.Frame):
                for w in widget.winfo_children():
                    if isinstance(w, tk.Label) and w.cget("text").endswith("%"):
                        percent_label = w
                        break
        def progress_callback(current, total):
            percent = int((current / total) * 90) if total > 0 else 0
            def update():
                progress["value"] = percent
                if percent_label:
                    percent_label["text"] = f"{percent}%"
            root.after(0, update)

        status_label.config(text="Extracting keyframes...", fg="#0070c0")
        progress["value"] = 0
        if percent_label:
            percent_label["text"] = "0%"
        keyframes = extract_keyframes(
            video_path, output_dir,
            diff_threshold=diff_threshold,
            sample_rate=sample_rate,
            min_interval=min_interval,
            stillness_threshold=stillness_threshold,
            stillness_frames=stillness_frames,
            progress_callback=progress_callback
        )
        def set_merging():
            status_label.config(text="Merging keyframes...", fg="#0070c0")
            progress["value"] = 95
            if percent_label:
                percent_label["text"] = "95%"
        root.after(0, set_merging)
        merged_path = os.path.join(output_dir, MERGED_IMAGE_PATH)
        merge_keyframes(keyframes, merged_path, max_per_row=5)
        def set_done():
            status_label.config(text="Completed! Saved to: " + output_dir, fg="green")
            progress["value"] = 100
            if percent_label:
                percent_label["text"] = "100%"
            open_btn.config(state="normal")
            open_btn.merged_path = merged_path
            messagebox.showinfo("Completed", f"Completed! Merged image saved to: {merged_path}")
        root.after(0, set_done)
    except Exception as e:
        def set_error():
            status_label.config(text="Error", fg="red")
            progress["value"] = 0
            if percent_label:
                percent_label["text"] = "0%"
            open_btn.config(state="disabled")
            messagebox.showerror("Error", str(e))
        root.after(0, set_error)

def start_extraction(
    video_path_var, output_dir_var, status_label, progress, root, open_btn,
    diff_threshold_var, sample_rate_var, min_interval_var, stillness_threshold_var, stillness_frames_var
):
    video_path = video_path_var.get()
    output_dir = output_dir_var.get()
    open_btn.config(state="disabled")
    if not video_path or not os.path.isfile(video_path):
        messagebox.showwarning("Please select a video", "Please select a correct MP4 video file.")
        return
    if not output_dir:
        messagebox.showwarning("Please select a folder", "Please select an output folder.")
        return
    progress["value"] = 0
    os.makedirs(output_dir, exist_ok=True)
    # Read slider values
    diff_threshold = diff_threshold_var.get()
    sample_rate = sample_rate_var.get()
    min_interval = min_interval_var.get()
    stillness_threshold = stillness_threshold_var.get()
    stillness_frames = stillness_frames_var.get()
    threading.Thread(
        target=run_extraction,
        args=(
            video_path, output_dir, status_label, progress, root, open_btn,
            diff_threshold, sample_rate, min_interval, stillness_threshold, stillness_frames
        ),
        daemon=True
    ).start()

def open_merged_image(btn):
    if hasattr(btn, "merged_path") and os.path.isfile(btn.merged_path):
        if sys.platform == "darwin":
            subprocess.call(["open", btn.merged_path])
        elif sys.platform == "win32":
            os.startfile(btn.merged_path)
        else:
            subprocess.call(["xdg-open", btn.merged_path])

def select_video(video_path_var, output_dir_var):
    path = filedialog.askopenfilename(title="Select Video", filetypes=VIDEO_EXTENSIONS)
    if path:
        video_path_var.set(path)
        # Use video filename (without extension) as Downloads subfolder
        base = os.path.splitext(os.path.basename(path))[0]
        new_dir = os.path.join(os.path.expanduser("~"), "Downloads", base)
        output_dir_var.set(new_dir)

def select_output_dir(output_dir_var):
    path = filedialog.askdirectory(title="Select Output Folder")
    if path:
        output_dir_var.set(path)

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".keyframe_extractor_config.json")
DEFAULT_PARAMS = {
    "diff_threshold": 25,
    "sample_rate": 24,
    "min_interval": 0.5,
    "stillness_threshold": 3,
    "stillness_frames": 5
}

def load_config():
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            # Check all keys exist, fill with default if missing
            for k, v in DEFAULT_PARAMS.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception:
            return DEFAULT_PARAMS.copy()
    else:
        return DEFAULT_PARAMS.copy()

def save_config(params):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(params, f)
    except Exception:
        pass

def main():
    root = tk.Tk()
    root.title("KeySnap Extractor")
    root.geometry("540x540")
    root.configure(bg="#eaf3fa")

    # Title
    title = tk.Label(root, text="KeySnap Extractor", bg="#eaf3fa", fg="#1a3a5e", font=("Arial Rounded MT Bold", 20, "bold"))
    title.pack(pady=(18, 2))

    subtitle = tk.Label(root, text="Automatic Keyframe Extraction and Merging Tool", bg="#eaf3fa", fg="#3e5c7f", font=("Arial", 12))
    subtitle.pack(pady=(0, 10))

    # Divider
    sep = tk.Frame(root, bg="#b5c9d6", height=2)
    sep.pack(fill="x", padx=30, pady=(0, 10))

    video_path_var = tk.StringVar()
    output_dir_var = tk.StringVar(value=DEFAULT_OUTPUT_DIR)

    # Video selection
    frame1 = tk.Frame(root, bg="#eaf3fa")
    frame1.pack(pady=(0, 5))
    tk.Label(frame1, text="Select MP4 Video:", bg="#eaf3fa", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 5))
    tk.Entry(frame1, textvariable=video_path_var, width=36, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame1, text="Browse...", command=lambda: select_video(video_path_var, output_dir_var), font=("Arial", 11), bg="#d0e3fa").pack(side=tk.LEFT, padx=(5, 0))

    # Output folder selection
    frame2 = tk.Frame(root, bg="#eaf3fa")
    frame2.pack(pady=(0, 5))
    tk.Label(frame2, text="Output Folder:", bg="#eaf3fa", font=("Arial", 12)).pack(side=tk.LEFT, padx=(0, 5))
    tk.Entry(frame2, textvariable=output_dir_var, width=36, font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
    tk.Button(frame2, text="Browse...", command=lambda: select_output_dir(output_dir_var), font=("Arial", 11), bg="#d0e3fa").pack(side=tk.LEFT, padx=(5, 0))

    # Parameter sliders
    param_frame = tk.LabelFrame(root, text="Extraction Parameters", bg="#eaf3fa", fg="#1a3a5e", font=("Arial", 12, "bold"), padx=10, pady=10)
    param_frame.pack(padx=30, pady=(10, 0), fill="x")

    config = load_config()

    # diff_threshold
    diff_threshold_var = tk.IntVar(value=config["diff_threshold"])
    tk.Label(param_frame, text="Frame Diff Threshold", bg="#eaf3fa", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
    diff_slider = tk.Scale(param_frame, from_=1, to=100, orient="horizontal", variable=diff_threshold_var, bg="#eaf3fa", length=200)
    diff_slider.grid(row=0, column=1, padx=5)
    tk.Label(param_frame, textvariable=diff_threshold_var, bg="#eaf3fa", width=4).grid(row=0, column=2)

    # sample_rate
    sample_rate_var = tk.IntVar(value=config["sample_rate"])
    tk.Label(param_frame, text="Sample Rate (fps)", bg="#eaf3fa", font=("Arial", 11)).grid(row=1, column=0, sticky="w")
    sample_slider = tk.Scale(param_frame, from_=1, to=60, orient="horizontal", variable=sample_rate_var, bg="#eaf3fa", length=200)
    sample_slider.grid(row=1, column=1, padx=5)
    tk.Label(param_frame, textvariable=sample_rate_var, bg="#eaf3fa", width=4).grid(row=1, column=2)

    # min_interval
    min_interval_var = tk.DoubleVar(value=config["min_interval"])
    tk.Label(param_frame, text="Min Interval (s)", bg="#eaf3fa", font=("Arial", 11)).grid(row=2, column=0, sticky="w")
    min_interval_slider = tk.Scale(param_frame, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", variable=min_interval_var, bg="#eaf3fa", length=200)
    min_interval_slider.grid(row=2, column=1, padx=5)
    tk.Label(param_frame, textvariable=min_interval_var, bg="#eaf3fa", width=4).grid(row=2, column=2)

    # stillness_threshold
    stillness_threshold_var = tk.IntVar(value=config["stillness_threshold"])
    tk.Label(param_frame, text="Stillness Threshold", bg="#eaf3fa", font=("Arial", 11)).grid(row=3, column=0, sticky="w")
    stillness_threshold_slider = tk.Scale(param_frame, from_=1, to=20, orient="horizontal", variable=stillness_threshold_var, bg="#eaf3fa", length=200)
    stillness_threshold_slider.grid(row=3, column=1, padx=5)
    tk.Label(param_frame, textvariable=stillness_threshold_var, bg="#eaf3fa", width=4).grid(row=3, column=2)

    # stillness_frames
    stillness_frames_var = tk.IntVar(value=config["stillness_frames"])
    tk.Label(param_frame, text="Stillness Frames", bg="#eaf3fa", font=("Arial", 11)).grid(row=4, column=0, sticky="w")
    stillness_frames_slider = tk.Scale(param_frame, from_=1, to=20, orient="horizontal", variable=stillness_frames_var, bg="#eaf3fa", length=200)
    stillness_frames_slider.grid(row=4, column=1, padx=5)
    tk.Label(param_frame, textvariable=stillness_frames_var, bg="#eaf3fa", width=4).grid(row=4, column=2)

    def update_config(*args):
        params = {
            "diff_threshold": diff_threshold_var.get(),
            "sample_rate": sample_rate_var.get(),
            "min_interval": min_interval_var.get(),
            "stillness_threshold": stillness_threshold_var.get(),
            "stillness_frames": stillness_frames_var.get()
        }
        save_config(params)

    # Auto-save when slider changes
    diff_threshold_var.trace_add("write", update_config)
    sample_rate_var.trace_add("write", update_config)
    min_interval_var.trace_add("write", update_config)
    stillness_threshold_var.trace_add("write", update_config)
    stillness_frames_var.trace_add("write", update_config)

    # Reset to Default button
    def reset_to_default():
        diff_threshold_var.set(DEFAULT_PARAMS["diff_threshold"])
        sample_rate_var.set(DEFAULT_PARAMS["sample_rate"])
        min_interval_var.set(DEFAULT_PARAMS["min_interval"])
        stillness_threshold_var.set(DEFAULT_PARAMS["stillness_threshold"])
        stillness_frames_var.set(DEFAULT_PARAMS["stillness_frames"])
        update_config()

    reset_btn = tk.Button(param_frame, text="Reset to Default", font=("Arial", 10, "bold"), bg="#f5d0d0", fg="#a33", command=reset_to_default)
    reset_btn.grid(row=5, column=0, columnspan=3, pady=(10, 0))

    # Status and progress
    status_label = tk.Label(root, text="", fg="#0070c0", bg="#eaf3fa", font=("Arial", 11, "bold"))
    status_label.pack(pady=(10, 0))

    progress_frame = tk.Frame(root, bg="#eaf3fa")
    progress_frame.pack(pady=(5, 0))
    progress = ttk.Progressbar(progress_frame, orient="horizontal", length=400, mode="determinate")
    progress.pack(side=tk.LEFT)
    percent_label = tk.Label(progress_frame, text="0%", bg="#eaf3fa", font=("Arial", 11, "bold"), width=5)
    percent_label.pack(side=tk.LEFT, padx=(8, 0))

    # Button colors
    PRIMARY_BG = "#1976d2"
    PRIMARY_BG_HOVER = "#2196f3"
    SUCCESS_BG = "#43a047"
    SUCCESS_BG_HOVER = "#66bb6a"

    btn_frame = tk.Frame(root, bg="#eaf3fa")
    btn_frame.pack(pady=(18, 0))

    # Create open_btn first, then set start_btn's command
    open_btn = tk.Button(btn_frame, text="Open Merged Image", width=18, height=2, bg=SUCCESS_BG, activebackground=SUCCESS_BG_HOVER,
                         fg="#0d2346", font=("Arial", 13, "bold"),
                         state="disabled", command=lambda: open_merged_image(open_btn))
    open_btn.pack(side=tk.RIGHT)

    def on_enter_open(e): open_btn.config(bg=SUCCESS_BG_HOVER)
    def on_leave_open(e): open_btn.config(bg=SUCCESS_BG)
    open_btn.bind("<Enter>", on_enter_open)
    open_btn.bind("<Leave>", on_leave_open)

    # Create start_btn, command can reference open_btn
    start_btn = tk.Button(
        btn_frame, text="Start Extraction", width=18, height=2, bg=PRIMARY_BG, activebackground=PRIMARY_BG_HOVER,
        fg="#0d2346", font=("Arial", 13, "bold"),
        command=lambda: start_extraction(
            video_path_var, output_dir_var, status_label, progress, root, open_btn,
            diff_threshold_var, sample_rate_var, min_interval_var, stillness_threshold_var, stillness_frames_var
        )
    )
    start_btn.pack(side=tk.RIGHT, padx=(0, 18))

    def on_enter_start(e): start_btn.config(bg=PRIMARY_BG_HOVER)
    def on_leave_start(e): start_btn.config(bg=PRIMARY_BG)
    start_btn.bind("<Enter>", on_enter_start)
    start_btn.bind("<Leave>", on_leave_start)

    # Footer
    footer = tk.Label(root, text="© 2025 KeySnap Extractor", bg="#eaf3fa", fg="#7a8fa6", font=("Arial", 9))
    footer.pack(side=tk.BOTTOM, pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    main()
