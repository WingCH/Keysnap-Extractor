# System Patterns – Keyframe Extractor

## System Architecture
- 單一 Python 應用，分為 CLI 與 GUI 兩種入口
- GUI 以 tkinter 為主，呼叫 extract_keyframes.py 之核心邏輯
- 影片處理與圖片合併邏輯集中於 extract_keyframes.py
- 打包流程以 py2app 為主，setup.py 定義 entry point

## Key Technical Decisions
- 使用 OpenCV 處理影片與影格差異判斷
- Pillow 負責圖片合併與文字標註
- Numpy 加速影像運算
- GUI 採用 tkinter，確保跨平台基礎
- macOS 打包選用 py2app，並明確記錄 tcl-tk/pyenv 依賴

## Design Patterns in Use
- MVC 淺層分離：GUI（View/Controller）與影片處理（Model/Logic）分開
- 多執行緒（threading）避免 GUI 卡死
- 參數預設與用戶可調（如 diff_threshold, sample_rate）

## Component Relationships
- extract_keyframes_gui.py：GUI 主程式，負責用戶互動與狀態顯示
- extract_keyframes.py：核心邏輯，負責影片分析與圖片合併
- setup.py：打包設定
- requirements.txt：依賴管理
- README.md：教學與 FAQ

## Critical Implementation Paths
- 用戶操作 GUI → 選擇影片/資料夾 → 點擊開始 → 執行 extract_keyframes → 合併圖片 → 顯示完成/錯誤
- 打包流程：pyenv 編譯 Python → venv 安裝依賴 → py2app 打包 → FAQ 排查
