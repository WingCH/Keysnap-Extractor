import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from extract_keyframes import extract_keyframes, merge_keyframes

VIDEO_EXTENSIONS = [("MP4 files", "*.mp4"), ("All files", "*.*")]
DEFAULT_OUTPUT_DIR = "keyframes"
MERGED_IMAGE_PATH = "keyframes_merged.png"

def run_extraction(video_path, output_dir, status_label, root):
    try:
        status_label.config(text="提取關鍵影格中...")
        keyframes = extract_keyframes(
            video_path, output_dir, diff_threshold=25, sample_rate=24, min_interval=0.5,
            stillness_threshold=3, stillness_frames=5
        )
        status_label.config(text="合併影格中...")
        merge_keyframes(keyframes, os.path.join(output_dir, MERGED_IMAGE_PATH), max_per_row=5)
        status_label.config(text="完成！已儲存於：" + output_dir)
        messagebox.showinfo("完成", f"已完成！合併圖片儲存於：{os.path.join(output_dir, MERGED_IMAGE_PATH)}")
    except Exception as e:
        status_label.config(text="發生錯誤")
        messagebox.showerror("錯誤", str(e))

def start_extraction(video_path_var, output_dir_var, status_label, root):
    video_path = video_path_var.get()
    output_dir = output_dir_var.get()
    if not video_path or not os.path.isfile(video_path):
        messagebox.showwarning("請選擇影片", "請選擇正確的 MP4 影片檔案。")
        return
    if not output_dir:
        messagebox.showwarning("請選擇資料夾", "請選擇輸出資料夾。")
        return
    threading.Thread(target=run_extraction, args=(video_path, output_dir, status_label, root), daemon=True).start()

def select_video(video_path_var):
    path = filedialog.askopenfilename(title="選擇影片", filetypes=VIDEO_EXTENSIONS)
    if path:
        video_path_var.set(path)

def select_output_dir(output_dir_var):
    path = filedialog.askdirectory(title="選擇輸出資料夾")
    if path:
        output_dir_var.set(path)

def main():
    root = tk.Tk()
    root.title("KeySnap Extractor")
    root.geometry("480x220")

    video_path_var = tk.StringVar()
    output_dir_var = tk.StringVar(value=DEFAULT_OUTPUT_DIR)

    tk.Label(root, text="選擇 MP4 影片：").pack(pady=(20, 0))
    frame1 = tk.Frame(root)
    frame1.pack()
    tk.Entry(frame1, textvariable=video_path_var, width=40).pack(side=tk.LEFT, padx=5)
    tk.Button(frame1, text="瀏覽...", command=lambda: select_video(video_path_var)).pack(side=tk.LEFT)

    tk.Label(root, text="選擇輸出資料夾：").pack(pady=(15, 0))
    frame2 = tk.Frame(root)
    frame2.pack()
    tk.Entry(frame2, textvariable=output_dir_var, width=40).pack(side=tk.LEFT, padx=5)
    tk.Button(frame2, text="瀏覽...", command=lambda: select_output_dir(output_dir_var)).pack(side=tk.LEFT)

    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack(pady=(15, 0))

    tk.Button(root, text="開始提取", width=20, height=2,
              command=lambda: start_extraction(video_path_var, output_dir_var, status_label, root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
