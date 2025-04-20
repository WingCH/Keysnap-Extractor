# Tech Context – Keyframe Extractor

## Technologies Used
- Python 3.12（推薦用 pyenv 編譯，支援 tcl-tk@8）
- OpenCV（cv2）：影片處理
- Pillow（PIL）：圖片合併與標註
- Numpy：影像運算
- tkinter：GUI
- py2app：macOS 打包
- pyenv、venv：Python 環境管理

## Development Setup
- 建議使用 Homebrew 安裝 pyenv、tcl-tk@8
- 以 pyenv 編譯 Python，確保 tkinter 支援
- venv 建立隔離環境，安裝 requirements.txt 依賴
- 開發流程可直接執行 extract_keyframes_gui.py 測試 GUI

## Technical Constraints
- macOS 打包需正確連結 tcl-tk@8，否則 tkinter 會缺失
- py2app 僅支援 macOS，Windows/Linux 打包需另行規劃
- 依賴需明確記錄於 requirements.txt
- GUI 以 tkinter 為主，外觀有限但跨平台

## Dependencies
- 依 requirements.txt 管理
- 主要依賴：opencv-python, pillow, numpy

## Tool Usage Patterns
- CLI/GUI 皆可用，GUI 以 tkinter 為主
- 打包流程詳見 README.md
- FAQ 與 troubleshooting 已納入文件
