import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import sys
import subprocess
from extract_keyframes import extract_keyframes, merge_keyframes

VIDEO_EXTENSIONS = [("MP4 files", "*.mp4"), ("All files", "*.*")]
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
MERGED_IMAGE_PATH = "keyframes_merged.png"

def run_extraction(video_path, output_dir, status_label, progress, root, open_btn):
    try:
        status_label.config(text="Extracting keyframes...", fg="#0070c0")
        progress["value"] = 20
        keyframes = extract_keyframes(
            video_path, output_dir, diff_threshold=25, sample_rate=24, min_interval=0.5,
            stillness_threshold=3, stillness_frames=5
        )
        status_label.config(text="Merging keyframes...", fg="#0070c0")
        progress["value"] = 70
        merged_path = os.path.join(output_dir, MERGED_IMAGE_PATH)
        merge_keyframes(keyframes, merged_path, max_per_row=5)
        status_label.config(text="Completed! Saved to: " + output_dir, fg="green")
        progress["value"] = 100
        open_btn.config(state="normal")
        open_btn.merged_path = merged_path
        messagebox.showinfo("Completed", f"Completed! Merged image saved to: {merged_path}")
    except Exception as e:
        status_label.config(text="Error", fg="red")
        progress["value"] = 0
        open_btn.config(state="disabled")
        messagebox.showerror("Error", str(e))

def start_extraction(video_path_var, output_dir_var, status_label, progress, root, open_btn):
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
    threading.Thread(target=run_extraction, args=(video_path, output_dir, status_label, progress, root, open_btn), daemon=True).start()

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
        # 以影片檔名（不含副檔名）作為 Downloads 子資料夾
        base = os.path.splitext(os.path.basename(path))[0]
        new_dir = os.path.join(os.path.expanduser("~"), "Downloads", base)
        output_dir_var.set(new_dir)

def select_output_dir(output_dir_var):
    path = filedialog.askdirectory(title="Select Output Folder")
    if path:
        output_dir_var.set(path)

def main():
    root = tk.Tk()
    root.title("KeySnap Extractor")
    root.geometry("540x320")
    root.configure(bg="#eaf3fa")

    # 標題
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

    # Status and progress
    status_label = tk.Label(root, text="", fg="#0070c0", bg="#eaf3fa", font=("Arial", 11, "bold"))
    status_label.pack(pady=(10, 0))

    progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=(5, 0))

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
    start_btn = tk.Button(btn_frame, text="Start Extraction", width=18, height=2, bg=PRIMARY_BG, activebackground=PRIMARY_BG_HOVER,
                          fg="#0d2346", font=("Arial", 13, "bold"),
                          command=lambda: start_extraction(video_path_var, output_dir_var, status_label, progress, root, open_btn))
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
