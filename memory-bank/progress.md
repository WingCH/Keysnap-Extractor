# Progress – Keyframe Extractor

## What works
- 影片自動提取關鍵影格、合併為單一圖片功能穩定
- GUI 介面（tkinter）已優化，支援進度條、狀態顏色、現代化配色
- macOS 打包（py2app）流程完整，FAQ 區塊協助新手排查
- 文件（README.md）結構完善，memory bank 已建立並同步

## What's left to build
- GUI 進一步美化（如圖片預覽、拖曳檔案、更多互動提示）
- Windows/Linux 打包教學與自動化腳本（Makefile、shell script）
- 更細緻的錯誤處理與用戶提示
- 定期同步 memory bank，確保知識不遺漏

## Current status
- 專案已可穩定運作，適合新手與一般用戶
- 交接文件與知識庫（memory bank）完整，便於團隊協作

## Known issues
- 目前僅 macOS 打包有完整教學，Windows/Linux 尚未支援
- GUI 外觀受限於 tkinter，進階美化需額外設計
- 影片格式僅支援 MP4，其他格式需後續擴充

## Evolution of project decisions
- 初期以 CLI 為主，後轉向 GUI 以提升易用性
- 打包流程多次優化，最終採用 pyenv + tcl-tk@8 + py2app
- FAQ 與 memory bank 納入專案標準流程，提升交接與維護效率
