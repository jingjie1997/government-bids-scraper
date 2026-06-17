## Context

台灣政府電子採購網（PCC）提供標案查詢功能，本系統需自動爬取勞務類 842 軟體執行服務的標案資料。PCC 網站為伺服器渲染頁面，查詢結果透過表單 POST 回傳 HTML，不使用 JavaScript 動態載入，因此可用 `requests` + `BeautifulSoup` 解析，無需瀏覽器自動化。

後端採 FastAPI 建置 REST API，對外提供觸發爬蟲與匯出 CSV 兩支端點。

## Goals / Non-Goals

**Goals:**
- 實作 PCC 標案爬蟲，依固定篩選條件（勞務類 842、標期內、關鍵字模糊搜尋）抓取資料
- 建立 FastAPI 後端，提供 `POST /api/scrape` 與 `GET /api/download-csv` 端點
- 支援 CORS，允許本地 React 前端呼叫
- 回傳標準化 JSON 格式資料

**Non-Goals:**
- 排程自動爬取（需使用者手動觸發）
- 資料持久化儲存（每次爬取結果暫存於記憶體，不寫入資料庫）
- 登入 / 身份驗證
- 前端實作（另立變更）

## Decisions

**1. 爬蟲工具：requests + BeautifulSoup（不用 Playwright）**

PCC 查詢結果頁為靜態 HTML，透過直接 POST 表單參數即可取得資料，不需執行 JavaScript。選擇 `requests` 可避免瀏覽器啟動開銷，部署也更簡單。

> 若日後 PCC 改為 AJAX 動態載入，則需切換至 Playwright。

**2. API 框架：FastAPI**

- 非同步支援，爬蟲期間不阻塞
- 自動產生 OpenAPI 文件，方便前端開發者查閱
- 輕量，啟動快速

**3. CSV 匯出：pandas**

資料已為結構化 list of dict，使用 `pandas.DataFrame.to_csv()` 可一行完成，輸出為 `StreamingResponse`，不需落地檔案。

**4. 資料暫存：記憶體（module-level 變數）**

爬蟲結果儲存在後端 module 層級的 list，`/api/scrape` 寫入、`/api/download-csv` 讀取。無持久化需求，簡化架構。

**5. 關鍵字搜尋策略：多次請求**

PCC 查詢介面每次只能輸入一個關鍵字，需分別對「系統開發」「系統維運」「系統建置」「專案建置」各發一次請求，合併結果後以標案案號去重。

## Risks / Trade-offs

- **PCC 網站結構變動** → HTML 解析邏輯需隨之更新，建議將選擇器集中在一個 `parser.py` 模組，降低維護成本
- **爬取速度 / 封鎖風險** → 多次請求間加入隨機延遲（0.5–1.5 秒），避免被擋
- **資料暫存遺失** → 後端重啟後需重新爬取，使用者需知悉（非 bug）
- **跨來源請求（CORS）** → 開發階段允許所有來源，正式部署需限縮為前端網域

## Migration Plan

1. 建立 `backend/` 目錄，初始化 Python 虛擬環境
2. 安裝相依套件並鎖定版本（`requirements.txt`）
3. 本地執行 `uvicorn main:app --reload` 驗證 API
4. 前端對接後，整合測試完成即可上線
5. 無資料庫，無需 migration script

## Open Questions

- PCC 網站是否需要帶 Cookie 或 User-Agent 才能正常回傳資料？（需實際測試確認）
- 每次搜尋結果筆數上限為何？是否需分頁爬取？
