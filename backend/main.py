import io

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from scraper import scrape_all, INDEX_URL, SEARCH_URL, HEADERS, _build_params, KEYWORDS

app = FastAPI(title="政府標案爬蟲 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_cached_bids: list = []

COLUMN_MAP = {
    "index": "項次",
    "agency": "機關名稱",
    "bid_number": "標案案號",
    "bid_name": "標案名稱",
    "procurement_method": "招標方式",
    "announcement_date": "公告日期",
    "deadline": "截止投標日期",
    "budget": "預算金額",
}


@app.get("/api/ping")
def ping():
    """健康檢查，確認伺服器正常運作。"""
    return {"status": "ok"}


@app.get("/api/debug")
def debug():
    """除錯端點：顯示爬蟲取得的原始 HTML 資訊，不做關鍵字過濾。"""
    try:
        session = requests.Session()
        session.get(INDEX_URL, headers=HEADERS, timeout=30)
        params = _build_params()
        params["pageIndex"] = "1"
        resp = session.get(SEARCH_URL, params=params, headers=HEADERS, timeout=30)
        resp.encoding = "utf-8"
        html = resp.text

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        table_info = [
            {"class": t.get("class"), "rows": len(t.find_all("tr"))}
            for t in tables
        ]

        # 找所有 td 列（不過濾關鍵字）
        # 找 tb_01 表格的第一筆資料列
        target_table = soup.find("table", {"class": "tb_01"})
        first_row_cell2_html = ""
        if target_table:
            data_rows = [r for r in target_table.find_all("tr") if r.find("td")]
            if data_rows:
                cells = data_rows[0].find_all("td")
                if len(cells) > 2:
                    first_row_cell2_html = str(cells[2])  # 標案案號+標案名稱欄位的原始 HTML

        all_rows = []
        for t in tables:
            for row in t.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) >= 7:
                    all_rows.append([c.get_text(strip=True) for c in cells])

        return {
            "http_status": resp.status_code,
            "html_length": len(html),
            "tables_found": len(tables),
            "table_info": table_info,
            "data_rows_found": len(all_rows),
            "first_3_rows": all_rows[:3],
            "cell2_raw_html": first_row_cell2_html,  # ← 這是關鍵：看 cells[2] 的原始 HTML
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/api/scrape")
def scrape():
    """觸發爬蟲，回傳標案清單 JSON。FastAPI 自動在 thread pool 執行同步函式。"""
    global _cached_bids
    try:
        _cached_bids = scrape_all()
        return {"data": _cached_bids, "count": len(_cached_bids)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/download-csv")
def download_csv():
    """將最近一次爬取結果以 CSV 格式回傳下載。"""
    if not _cached_bids:
        return JSONResponse(
            status_code=404,
            content={"error": "尚無資料，請先執行爬取"},
        )

    df = pd.DataFrame(_cached_bids).rename(columns=COLUMN_MAP)
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding="utf-8-sig")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=bids.csv"},
    )
