## Purpose

Bids API 模組提供 Flask REST API，供前端呼叫以觸發爬蟲、取得標案資料，並支援 CSV 下載。模組負責 CORS 設定及統一的 JSON 回傳格式。

## Requirements

### Requirement: 觸發爬蟲端點
系統 SHALL 提供 `POST /api/scrape` 端點，供前端呼叫以觸發後端爬蟲並取得標案清單。

#### Scenario: 成功觸發並回傳資料
- **WHEN** 前端呼叫 `POST /api/scrape`
- **THEN** 系統 SHALL 執行爬蟲、暫存結果，並回傳 HTTP 200 及 JSON 格式的標案陣列，結構為 `{ "data": [...], "count": N }`

#### Scenario: 爬蟲執行中錯誤處理
- **WHEN** 爬蟲過程中發生網路錯誤或解析失敗
- **THEN** 系統 SHALL 回傳 HTTP 500 及錯誤訊息 JSON `{ "error": "<說明>" }`

### Requirement: CSV 下載端點
系統 SHALL 提供 `GET /api/download-csv` 端點，將最近一次爬取結果以 CSV 格式回傳供下載。

#### Scenario: 成功下載 CSV
- **WHEN** 前端呼叫 `GET /api/download-csv`，且已有爬取結果暫存
- **THEN** 系統 SHALL 回傳 HTTP 200、Content-Type 為 `text/csv`、Content-Disposition 含檔名 `bids.csv`，內容包含標頭列與所有資料列

#### Scenario: 尚無資料時下載
- **WHEN** 前端呼叫 `GET /api/download-csv`，但尚未執行爬蟲
- **THEN** 系統 SHALL 回傳 HTTP 404 及訊息 `{ "error": "尚無資料，請先執行爬取" }`

### Requirement: CORS 支援
系統 SHALL 啟用 CORS，允許前端（React 開發伺服器）跨來源呼叫 API。

#### Scenario: 前端跨來源請求
- **WHEN** React 前端從不同 port 呼叫後端 API
- **THEN** 系統 SHALL 在回應標頭中包含適當的 `Access-Control-Allow-Origin`，使瀏覽器不阻擋請求

### Requirement: JSON 回傳格式
系統 SHALL 以統一的 JSON 結構回傳標案資料，每筆資料包含固定欄位。

#### Scenario: 標案資料結構驗證
- **WHEN** `POST /api/scrape` 成功回傳資料
- **THEN** 每筆標案物件 SHALL 包含以下鍵值：`index`、`agency`、`bid_number`、`bid_name`、`procurement_method`、`announcement_date`、`deadline`、`budget`
