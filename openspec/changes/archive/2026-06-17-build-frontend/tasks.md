## 1. 前端專案初始化

- [x] 1.1 在 `frontend/` 目錄使用 Vite 建立 React 專案（`npm create vite@latest frontend -- --template react`）
- [x] 1.2 進入 `frontend/` 安裝依賴（`npm install`）
- [x] 1.3 設定 `vite.config.js`：新增 server proxy，將 `/api` 轉發至 `http://127.0.0.1:8000`

## 2. 主頁面元件實作

- [x] 2.1 清空 Vite 預設範本內容（`App.jsx`、`App.css`、`index.css`），保留乾淨起點
- [x] 2.2 在 `App.jsx` 實作「爬取標案」按鈕：點擊後呼叫 `POST /api/scrape`，觸發期間按鈕 disabled 並顯示「爬取中…」
- [x] 2.3 實作載入狀態管理：使用 `useState` 管理 `loading`、`bids`、`error` 三個狀態
- [x] 2.4 實作錯誤顯示：API 失敗時在頁面顯示錯誤訊息

## 3. 標案資料表格

- [x] 3.1 實作 `BidsTable` 元件，接收 `bids` 陣列 prop，渲染含八個欄位的 HTML 表格（項次、機關名稱、標案案號、標案名稱、招標方式、公告日期、截止投標日期、預算金額）
- [x] 3.2 處理空資料情境：`bids` 為空陣列時顯示「無符合條件的標案」提示
- [x] 3.3 在 `App.jsx` 引入並條件渲染 `BidsTable`（有資料才顯示）

## 4. CSV 下載功能

- [x] 4.1 實作「下載 CSV」按鈕：呼叫 `window.location.href = '/api/download-csv'` 觸發瀏覽器下載
- [x] 4.2 未執行爬取或 `bids` 為空時，「下載 CSV」按鈕 disabled

## 5. 樣式與驗收

- [x] 5.1 為頁面加入基本 CSS：標題、按鈕間距、表格樣式（邊框、交替列背景）
- [x] 5.2 本地啟動前後端（後端：`uvicorn main:app --reload`，前端：`npm run dev`），在瀏覽器實測完整流程：爬取 → 表格顯示 → CSV 下載
- [x] 5.3 確認錯誤情境：關閉後端後點擊爬取，確認前端顯示錯誤訊息
