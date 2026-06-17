## Context

後端 FastAPI 已在 `http://127.0.0.1:8000` 提供完整 API，本次僅需建置 React 前端，無需修改任何後端程式碼。前端與後端為獨立程序，透過 HTTP 溝通。

## Goals / Non-Goals

**Goals:**
- 建立 `frontend/` React 專案（Vite）
- 實作爬取按鈕、標案表格、CSV 下載、載入與錯誤狀態
- 前端開發時透過 Vite proxy 轉發 API 請求，避免 CORS 問題

**Non-Goals:**
- 分頁、排序、搜尋等進階表格功能
- 使用者驗證
- 部署至遠端主機

## Decisions

**1. 使用 Vite + React（不使用 Create React App）**
Vite 啟動速度快、設定簡單，且原生支援 proxy 設定，適合快速建立前端開發環境。

**2. 不引入狀態管理函式庫（useState + fetch 即可）**
資料流單純：觸發爬取 → 存入 state → 渲染表格。無需 Redux 或 Zustand 的額外複雜度。

**3. Vite dev proxy 轉發 `/api` 至後端**
開發時前端跑在 `localhost:5173`，直接呼叫 `localhost:8000` 會受瀏覽器 CORS 限制（雖後端已開放，但統一走 proxy 更乾淨）。`vite.config.js` 設定 `/api` → `http://127.0.0.1:8000`。

**4. CSV 下載用 `window.location.href`**
`GET /api/download-csv` 回傳 `Content-Disposition: attachment`，直接導向該 URL 讓瀏覽器觸發下載，無需 Blob 處理。

**5. 不引入 UI 元件庫**
以原生 HTML + 基本 CSS 實作，保持最小依賴。

## Risks / Trade-offs

- **後端未啟動時前端無法運作** → 文件說明需先啟動後端；錯誤訊息提示使用者確認後端狀態
- **爬蟲耗時較長（數秒）** → 按鈕 disabled + 顯示「爬取中…」避免重複觸發

## Migration Plan

1. 在 `frontend/` 建立 Vite React 專案
2. 設定 `vite.config.js` proxy
3. 實作主頁面元件
4. 前端開發伺服器：`npm run dev`（port 5173）
5. 後端保持獨立啟動：`uvicorn main:app --reload`（port 8000）
