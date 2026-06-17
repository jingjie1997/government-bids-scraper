## Why

後端 API 已完成，目前缺少使用者介面，使用者無法透過瀏覽器操作爬蟲、瀏覽結果或下載資料。建置 React 前端是讓系統可實際使用的最後一哩路。

## What Changes

- 新增 `frontend/` 目錄，使用 Vite + React 建立前端專案
- 實作「爬取標案」按鈕，點擊後呼叫後端 `POST /api/scrape`
- 爬取完成後，以表格顯示標案清單（項次、機關名稱、標案案號、標案名稱、招標方式、公告日期、截止投標日期、預算金額）
- 實作「下載 CSV」按鈕，呼叫 `GET /api/download-csv` 觸發瀏覽器下載
- 顯示載入中狀態與錯誤提示

## Capabilities

### New Capabilities

- `bid-table-ui`：標案資料表格顯示與互動介面，包含爬取按鈕、表格渲染、CSV 下載、載入與錯誤狀態

### Modified Capabilities

（無）

## Impact

- 新增 `frontend/` 目錄（Vite + React 專案）
- 依賴後端 `POST /api/scrape` 與 `GET /api/download-csv`
- 後端需維持 CORS 開放（已設定）
- 不異動任何後端程式碼
