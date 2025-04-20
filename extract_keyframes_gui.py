import sys
import os
import json
import threading
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QProgressBar, QSlider, QLineEdit, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from extract_keyframes import extract_keyframes, merge_keyframes

VIDEO_EXTENSIONS = "Video Files (*.mp4 *.avi *.mov)"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
MERGED_IMAGE_PATH = "keyframes_merged.png"
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".keyframe_extractor_config.json")
DEFAULT_PARAMS = {
    "diff_threshold": 25,
    "sample_rate": 24,
    "min_interval": 0.5,  # 0.1~5.0, slider 1~50, value/10
    "stillness_threshold": 3,
    "stillness_frames": 5
}

def load_config():
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
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

class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    status = pyqtSignal(str, str)
    finished = pyqtSignal(str)

class ExtractionWorker(threading.Thread):
    def __init__(self, video_path, output_dir, params, signals):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.params = params
        self.signals = signals

    def run(self):
        try:
            def progress_callback(current, total):
                percent = int((current / total) * 90) if total > 0 else 0
                self.signals.progress.emit(percent)
            self.signals.status.emit("Extracting keyframes...", "#0070c0")
            keyframes = extract_keyframes(
                self.video_path, self.output_dir,
                diff_threshold=self.params["diff_threshold"],
                sample_rate=self.params["sample_rate"],
                min_interval=self.params["min_interval"] / 10.0,
                stillness_threshold=self.params["stillness_threshold"],
                stillness_frames=self.params["stillness_frames"],
                progress_callback=progress_callback
            )
            self.signals.status.emit("Merging keyframes...", "#0070c0")
            self.signals.progress.emit(95)
            merged_path = os.path.join(self.output_dir, MERGED_IMAGE_PATH)
            merge_keyframes(keyframes, merged_path, max_per_row=5)
            self.signals.status.emit(f"Completed! Saved to: {self.output_dir}", "green")
            self.signals.progress.emit(100)
            self.signals.finished.emit(merged_path)
        except Exception as e:
            self.signals.status.emit("Error: " + str(e), "red")
            self.signals.progress.emit(0)
            self.signals.finished.emit("")

class KeyframeExtractorV2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeySnap Extractor")
        self.setWindowIcon(QIcon("app_icon.png"))
        self.setMinimumWidth(600)
        self.params = load_config()
        self.selected_file = ""
        self.output_dir = DEFAULT_OUTPUT_DIR
        self.merged_path = ""
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        title = QLabel("KeySnap Extractor")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1a3a5e;")
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel("Automatic Keyframe Extraction and Merging Tool")
        subtitle.setStyleSheet("color: #3e5c7f; font-size: 13px;")
        main_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        # Video selection
        file_layout = QHBoxLayout()
        self.setAcceptDrops(True)
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Select a video file")
        file_layout.addWidget(self.file_edit)
        file_btn = QPushButton("Browse Video")
        file_btn.clicked.connect(self.select_video)
        file_layout.addWidget(file_btn)
        main_layout.addLayout(file_layout)

        # Output folder selection
        out_layout = QHBoxLayout()
        self.out_edit = QLineEdit()
        self.out_edit.setText(self.output_dir)
        out_layout.addWidget(self.out_edit)
        out_btn = QPushButton("Browse Output Folder")
        out_btn.clicked.connect(self.select_output_dir)
        out_layout.addWidget(out_btn)
        main_layout.addLayout(out_layout)

        # Parameter controls (sliders)
        param_group = QGroupBox("Extraction Parameters")
        param_layout = QVBoxLayout()

        # diff_threshold
        self.diff_slider = QSlider(Qt.Horizontal)
        self.diff_slider.setRange(1, 100)
        self.diff_slider.setValue(self.params["diff_threshold"])
        self.diff_label = QLabel(f"{self.diff_slider.value()}")
        self._add_slider_row(param_layout, "Frame Diff Threshold", self.diff_slider, self.diff_label)

        # sample_rate
        self.sample_slider = QSlider(Qt.Horizontal)
        self.sample_slider.setRange(1, 60)
        self.sample_slider.setValue(self.params["sample_rate"])
        self.sample_label = QLabel(f"{self.sample_slider.value()}")
        self._add_slider_row(param_layout, "Sample Rate (fps)", self.sample_slider, self.sample_label)

        # min_interval (0.1~5.0, step 0.1, slider 1~50, value/10)
        self.min_interval_slider = QSlider(Qt.Horizontal)
        self.min_interval_slider.setRange(1, 50)
        self.min_interval_slider.setValue(int(round(self.params["min_interval"] * 10)))
        self.min_interval_label = QLabel(f"{self.min_interval_slider.value()/10:.1f}")
        self._add_slider_row(param_layout, "Min Interval (s)", self.min_interval_slider, self.min_interval_label)

        # stillness_threshold
        self.stillness_threshold_slider = QSlider(Qt.Horizontal)
        self.stillness_threshold_slider.setRange(1, 20)
        self.stillness_threshold_slider.setValue(self.params["stillness_threshold"])
        self.stillness_threshold_label = QLabel(f"{self.stillness_threshold_slider.value()}")
        self._add_slider_row(param_layout, "Stillness Threshold", self.stillness_threshold_slider, self.stillness_threshold_label)

        # stillness_frames
        self.stillness_frames_slider = QSlider(Qt.Horizontal)
        self.stillness_frames_slider.setRange(1, 20)
        self.stillness_frames_slider.setValue(self.params["stillness_frames"])
        self.stillness_frames_label = QLabel(f"{self.stillness_frames_slider.value()}")
        self._add_slider_row(param_layout, "Stillness Frames", self.stillness_frames_slider, self.stillness_frames_label)

        # Reset button
        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_params)
        param_layout.addWidget(reset_btn)

        param_group.setLayout(param_layout)
        main_layout.addWidget(param_group)

        # Status and progress
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #0070c0; font-weight: bold;")
        main_layout.addWidget(self.status_label)

        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        self.percent_label = QLabel("0%")
        progress_layout.addWidget(self.percent_label)
        main_layout.addLayout(progress_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Extraction")
        self.start_btn.clicked.connect(self.start_extraction)
        btn_layout.addWidget(self.start_btn)

        self.open_btn = QPushButton("Open Merged Image")
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self.open_merged_image)
        btn_layout.addWidget(self.open_btn)
        main_layout.addLayout(btn_layout)

        # Footer
        footer = QLabel("© 2025 KeySnap Extractor")
        footer.setStyleSheet("color: #7a8fa6; font-size: 10px;")
        main_layout.addWidget(footer, alignment=Qt.AlignRight)

        self.setLayout(main_layout)
        self.connect_param_signals()

    def _add_slider_row(self, layout, label_text, slider, value_label):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(140)
        row.addWidget(label)
        row.addWidget(slider)
        row.addWidget(value_label)
        layout.addLayout(row)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith(('.mp4', '.avi', '.mov')):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                    self.file_edit.setText(file_path)
                    # 自動命名 output folder
                    base = os.path.splitext(os.path.basename(file_path))[0]
                    new_dir = os.path.join(os.path.expanduser("~"), "Downloads", base)
                    self.out_edit.setText(new_dir)
                    self.output_dir = new_dir
        event.acceptProposedAction()

    def connect_param_signals(self):
        self.diff_slider.valueChanged.connect(lambda v: self._on_slider_change("diff_threshold", v, self.diff_label))
        self.sample_slider.valueChanged.connect(lambda v: self._on_slider_change("sample_rate", v, self.sample_label))
        self.min_interval_slider.valueChanged.connect(lambda v: self._on_slider_change("min_interval", v, self.min_interval_label, True))
        self.stillness_threshold_slider.valueChanged.connect(lambda v: self._on_slider_change("stillness_threshold", v, self.stillness_threshold_label))
        self.stillness_frames_slider.valueChanged.connect(lambda v: self._on_slider_change("stillness_frames", v, self.stillness_frames_label))

    def _on_slider_change(self, param, value, label_widget, is_float=False):
        if is_float:
            label_widget.setText(f"{value/10:.1f}")
        else:
            label_widget.setText(str(value))
        self.save_params()

    def save_params(self):
        self.params = {
            "diff_threshold": self.diff_slider.value(),
            "sample_rate": self.sample_slider.value(),
            "min_interval": self.min_interval_slider.value() / 10.0,
            "stillness_threshold": self.stillness_threshold_slider.value(),
            "stillness_frames": self.stillness_frames_slider.value()
        }
        save_config(self.params)

    def reset_params(self):
        self.diff_slider.setValue(DEFAULT_PARAMS["diff_threshold"])
        self.sample_slider.setValue(DEFAULT_PARAMS["sample_rate"])
        self.min_interval_slider.setValue(int(round(DEFAULT_PARAMS["min_interval"] * 10)))
        self.min_interval_label.setText(f"{DEFAULT_PARAMS['min_interval']:.1f}")
        self.stillness_threshold_slider.setValue(DEFAULT_PARAMS["stillness_threshold"])
        self.stillness_frames_slider.setValue(DEFAULT_PARAMS["stillness_frames"])
        self.save_params()

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇影片", "", VIDEO_EXTENSIONS)
        if file_path:
            self.selected_file = file_path
            self.file_edit.setText(file_path)
            # 自動命名 output folder
            base = os.path.splitext(os.path.basename(file_path))[0]
            new_dir = os.path.join(os.path.expanduser("~"), "Downloads", base)
            self.out_edit.setText(new_dir)
            self.output_dir = new_dir

    def select_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "選擇輸出資料夾", DEFAULT_OUTPUT_DIR)
        if dir_path:
            self.output_dir = dir_path
            self.out_edit.setText(dir_path)

    def start_extraction(self):
        video_path = self.file_edit.text()
        output_dir = self.out_edit.text()
        if not video_path or not os.path.isfile(video_path):
            QMessageBox.warning(self, "Error", "Please select a valid video file.")
            return
        if not output_dir:
            QMessageBox.warning(self, "Error", "Please select an output folder.")
            return
        os.makedirs(output_dir, exist_ok=True)
        self.status_label.setText("準備中...")
        self.progress_bar.setValue(0)
        self.percent_label.setText("0%")
        self.open_btn.setEnabled(False)
        params = {
            "diff_threshold": self.diff_slider.value(),
            "sample_rate": self.sample_slider.value(),
            "min_interval": self.min_interval_slider.value(),
            "stillness_threshold": self.stillness_threshold_slider.value(),
            "stillness_frames": self.stillness_frames_slider.value()
        }
        self.save_params()
        self.worker_signals = WorkerSignals()
        self.worker_signals.progress.connect(self.update_progress)
        self.worker_signals.status.connect(self.update_status)
        self.worker_signals.finished.connect(self.extraction_finished)
        self.worker = ExtractionWorker(video_path, output_dir, params, self.worker_signals)
        self.worker.start()

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)
        self.percent_label.setText(f"{percent}%")

    def update_status(self, text, color):
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")

    def extraction_finished(self, merged_path):
        if merged_path and os.path.isfile(merged_path):
            self.merged_path = merged_path
            self.open_btn.setEnabled(True)
            QMessageBox.information(self, "Completed", f"Keyframe extraction and merging completed.\n\nMerged image saved at:\n{merged_path}")
        else:
            self.open_btn.setEnabled(False)

    def open_merged_image(self):
        if self.merged_path and os.path.isfile(self.merged_path):
            if sys.platform == "darwin":
                subprocess.call(["open", self.merged_path])
            elif sys.platform == "win32":
                os.startfile(self.merged_path)
            else:
                subprocess.call(["xdg-open", self.merged_path])

import signal
from PyQt5.QtCore import QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KeyframeExtractorV2()
    window.show()

    # Allow Ctrl+C to quit the app in terminal (QTimer workaround for macOS/VSCode)
    signal.signal(signal.SIGINT, lambda *args: app.quit())
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    sys.exit(app.exec_())
