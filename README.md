# 政府標案爬蟲系統

自動爬取台灣[政府電子採購網（PCC）](https://web.pcc.gov.tw)的勞務類標案，篩選軟體開發相關案件，透過 React 前端介面顯示結果並支援 CSV 下載。

## 功能

- 爬取勞務類 842（軟體執行服務）、等標期內的所有標案（自動翻頁）
- 依關鍵字過濾：**系統開發、系統維運、系統建置、專案建置、維護、維運**
- 繞過 PCC `pageCode2Img` 圖片反爬機制，直接從 HTML 提取標案名稱
- React 前端介面：爬取按鈕、標案表格、CSV 下載
- **關鍵字排除按鈕**：點選「設備」「機房」「醫院」「儀器」可即時從結果中排除含該關鍵字的標案，支援多選（OR 邏輯），項次自動重新計算
- REST API：供前端或第三方工具呼叫

## 技術架構

| 層級 | 技術 |
|------|------|
| 後端 | Python 3 · FastAPI · requests · BeautifulSoup4 · pandas |
| 前端 | React · Vite |

## 快速開始

### 環境需求

- Python 3.9+
- Node.js 18+

### 後端安裝與啟動

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# 必須在 backend/ 目錄下執行
uvicorn main:app --reload
```

後端啟動於 `http://127.0.0.1:8000`

### 前端安裝與啟動

```bash
cd frontend
npm install
npm run dev
```

前端啟動於 `http://localhost:5173`（若 port 被占用會自動遞增）

> 前端透過 Vite proxy 轉發 `/api` 請求至後端，請確保後端已先啟動。

## 使用方式

1. 啟動後端與前端
2. 開啟瀏覽器前往 `http://localhost:5173`
3. 點擊「爬取標案」按鈕
4. 等待爬取完成，結果以表格顯示
5. （選用）點擊「設備」「機房」「醫院」「儀器」排除按鈕，過濾不相關的標案；可多選，再點一次取消
6. 點擊「下載 CSV」儲存目前表格顯示的資料（已套用排除篩選）

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/api/ping` | 健康檢查 |
| `POST` | `/api/scrape` | 觸發爬蟲，回傳標案 JSON |
| `GET` | `/api/download-csv` | 下載最近一次爬取結果（CSV，後端全量；前端介面改用 Blob 下載篩選後資料） |

### 回傳格式（/api/scrape）

```json
{
  "data": [
    {
      "index": 1,
      "agency": "某政府機關",
      "bid_number": "113-001",
      "bid_name": "系統維運服務採購案",
      "procurement_method": "公開招標",
      "announcement_date": "2026/06/01",
      "deadline": "2026/06/30",
      "budget": "1,000,000"
    }
  ],
  "count": 1
}
```

## 專案結構

```
government_bids_scraper/
├── backend/
│   ├── main.py          # FastAPI 應用程式與 API 端點
│   ├── scraper.py       # PCC 爬蟲邏輯（含翻頁、關鍵字過濾）
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # 主頁面元件
│   │   └── BidsTable.jsx # 標案表格元件
│   ├── vite.config.js   # Vite 設定（含 /api proxy）
│   └── package.json
├── openspec/            # 規格文件（OpenSpec 工作流）
│   ├── config.yaml
│   ├── specs/           # 主規格庫
│   └── changes/         # 變更紀錄與封存
└── README.md
```

## 注意事項

- 本工具僅供學術研究與個人使用，請遵守 PCC 網站使用規範
- 爬蟲涵蓋過去 90 天內公告、目前仍在等標期內的標案，翻頁間加入隨機延遲避免對伺服器造成壓力
