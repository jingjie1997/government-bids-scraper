# 政府標案爬蟲系統

自動爬取台灣[政府電子採購網（PCC）](https://web.pcc.gov.tw)的勞務類標案，篩選軟體開發相關案件，並提供 REST API 供前端呼叫。

## 功能

- 爬取勞務類 842（軟體執行服務）、等標期內的所有標案
- 依關鍵字過濾：**系統開發、系統維運、系統建置、專案建置**
- 繞過 PCC `pageCode2Img` 圖片反爬機制，直接從 HTML 提取標案名稱
- 提供 REST API：觸發爬蟲、回傳 JSON、下載 CSV

## 技術架構

| 層級 | 技術 |
|------|------|
| 後端 | Python 3 · FastAPI · requests · BeautifulSoup4 |
| 前端 | React（開發中） |

## 快速開始

### 環境需求

- Python 3.9+

### 安裝

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 啟動後端

```bash
# 必須在 backend/ 目錄下執行
cd backend
uvicorn main:app --reload
```

伺服器啟動於 `http://127.0.0.1:8000`

## API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/api/ping` | 健康檢查 |
| `POST` | `/api/scrape` | 觸發爬蟲，回傳標案 JSON |
| `GET` | `/api/download-csv` | 下載最近一次爬取結果（CSV） |

### 範例

```bash
# 觸發爬蟲
curl -X POST http://127.0.0.1:8000/api/scrape

# 下載 CSV
curl http://127.0.0.1:8000/api/download-csv -o bids.csv
```

### 回傳格式（/api/scrape）

```json
{
  "data": [
    {
      "index": 1,
      "agency": "某政府機關",
      "bid_number": "113-001",
      "bid_name": "系統開發採購案",
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
│   ├── scraper.py       # PCC 爬蟲邏輯
│   └── requirements.txt
├── openspec/            # 規格文件（OpenSpec 工作流）
│   ├── config.yaml
│   ├── specs/           # 主規格庫
│   └── changes/         # 變更紀錄與封存
└── README.md
```

## 注意事項

- 本工具僅供學術研究與個人使用，請遵守 PCC 網站使用規範
- 爬蟲每次搜尋涵蓋過去 90 天內公告的等標期內標案
- 前端（React）開發中，目前可直接呼叫 API 或等待前端完成
