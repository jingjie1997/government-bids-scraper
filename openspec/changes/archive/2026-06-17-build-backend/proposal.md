## Why

目前沒有任何工具可以自動從台灣政府電子採購網（PCC）篩選出軟體執行服務類標案，使用者需要手動進入網站逐頁查詢，耗時且容易遺漏。本專案建置一套後端爬蟲 API，讓使用者一鍵取得最新標期內的相關標案資料。

## What Changes

- 新增 Python 後端服務，提供 RESTful API
- 實作爬蟲邏輯，爬取 PCC 勞務類 842（軟體執行服務）標案
- 篩選條件：日期選擇「標期內」，標案名稱關鍵字模糊搜尋包含「系統開發、系統維運、系統建置、專案建置」
- 回傳結構化 JSON 資料（項次、機關名稱、標案案號、標案名稱、招標方式、公告日期、截止投標日期、預算金額）
- 提供 CSV 匯出 API endpoint

## Capabilities

### New Capabilities

- `pcc-scraper`：爬取 PCC 政府電子採購網，依指定篩選條件抓取標案清單並回傳結構化資料
- `bids-api`：RESTful API 層，提供「觸發爬蟲」與「下載 CSV」兩支端點供前端呼叫

### Modified Capabilities

（無，本次為全新建置）

## Impact

- 新增後端目錄結構（`backend/`）
- 相依套件：`requests` 或 `playwright`（視 PCC 網站是否需要 JS 渲染而定）、`fastapi`、`uvicorn`、`pandas`（CSV 匯出）
- 對外暴露兩支 API：
  - `POST /api/scrape`：觸發爬蟲，回傳標案清單 JSON
  - `GET /api/download-csv`：回傳 CSV 檔案
- 前端須配合呼叫上述 API（前端實作為後續變更）
