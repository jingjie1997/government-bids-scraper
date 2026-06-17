## 1. 後端專案初始化

- [x] 1.1 建立 `backend/` 目錄，初始化 Python 虛擬環境（`python -m venv venv`）
- [x] 1.2 建立 `backend/requirements.txt`，加入 `fastapi`、`uvicorn`、`requests`、`beautifulsoup4`、`pandas`
- [x] 1.3 建立 `backend/main.py`，設定 FastAPI app 與 CORS middleware（允許所有來源）

## 2. 爬蟲模組實作

- [x] 2.1 建立 `backend/scraper.py`，實作 `fetch_page(keyword)` 函式：向 PCC 發送 POST 請求，帶入勞務類 842、標期內、關鍵字參數，回傳 HTML 字串
- [x] 2.2 實作 `parse_bids(html)` 函式：解析 HTML，提取每筆標案的八個欄位（項次、機關名稱、標案案號、標案名稱、招標方式、公告日期、截止投標日期、預算金額），回傳 list of dict
- [x] 2.3 實作 `scrape_all()` 函式：依序對四個關鍵字（系統開發、系統維運、系統建置、專案建置）呼叫 `fetch_page` + `parse_bids`，合併結果後以標案案號去重，回傳最終清單
- [x] 2.4 在每次 `fetch_page` 呼叫之間加入 0.5–1.5 秒隨機延遲

## 3. API 端點實作

- [x] 3.1 在 `backend/main.py` 實作 `POST /api/scrape`：呼叫 `scrape_all()`、暫存結果至 module-level 變數，回傳 `{ "data": [...], "count": N }`
- [x] 3.2 實作 `GET /api/download-csv`：若暫存資料為空回傳 404，否則用 pandas 將資料轉為 CSV，以 `StreamingResponse` 回傳，Content-Disposition 設為 `attachment; filename=bids.csv`

## 4. 驗證與測試

- [x] 4.1 本地啟動 `uvicorn main:app --reload`，以 curl 或瀏覽器測試 `POST /api/scrape` 確認能成功爬取並回傳資料
- [x] 4.2 測試 `GET /api/download-csv` 確認 CSV 內容正確、欄位齊全
- [x] 4.3 測試無資料時 `GET /api/download-csv` 回傳 404
- [x] 4.4 確認四個關鍵字均有搜尋、結果去重正確
