"""
PCC 政府電子採購網爬蟲

查詢方式：GET 請求，搜尋全部勞務類 842 等標期內標案，
再於 Python 端依關鍵字過濾標案名稱。
"""

import re
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

INDEX_URL = "https://web.pcc.gov.tw/prkms/tender/common/proctrg/indexTenderProctrg"
SEARCH_URL = "https://web.pcc.gov.tw/prkms/tender/common/proctrg/readTenderProctrg"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": INDEX_URL,
}

# 標案名稱過濾關鍵字（在爬取結果後本地過濾）
KEYWORDS = ["系統開發", "系統維運", "系統建置", "專案建置", "維護", "維運"]


def _build_params() -> Dict[str, str]:
    """
    組建 PCC 搜尋 GET 參數（依實際網站 URL 確認）。
    日期範圍：過去 90 天到今天，涵蓋所有目前等標期內的標案。
    """
    today = datetime.now()
    start = today - timedelta(days=90)
    return {
        "pageSize": "100",
        "firstSearch": "false",
        "searchType": "tpam",
        "isBinding": "N",
        "isLogIn": "N",
        "level_1": "on",
        "tenderStatus": "TENDER_STATUS_0",          # 等標期內
        "tenderWay": "TENDER_WAY_ALL_DECLARATION",  # 各式招標公告
        "proctrgCode1": "",
        "proctrgCode2": "",
        "radProctrgCate": "RAD_PROCTRG_CATE_3",     # 勞務類
        "proctrgCode3": "50003065",                  # 842 軟體執行服務
        "dateType": "isSpdt",
        "tenderStartDate": start.strftime("%Y/%m/%d"),
        "tenderEndDate": today.strftime("%Y/%m/%d"),
    }


def fetch_page(session: requests.Session, page: int = 1) -> str:
    """向 PCC 送出 GET 搜尋請求，回傳 HTML 字串。"""
    params = _build_params()
    params["pageIndex"] = str(page)
    response = session.get(
        SEARCH_URL,
        params=params,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()
    response.encoding = "utf-8"
    return response.text


def _extract_bid_name(row) -> str:
    """
    從該列所有 <script> 標籤中取出標案名稱。
    PCC 將中文名稱傳入 pageCode2Img() 轉成圖片防爬，但文字仍保留在 HTML 中。
    """
    for script in row.find_all("script"):
        text = script.string or ""
        match = re.search(r'pageCode2Img\("([^"]+)"\)', text)
        if match:
            return match.group(1)
    return ""


def parse_bids(html: str) -> List[Dict]:
    """
    解析 PCC 標的分類查詢 HTML。

    實測欄位順序（tb_01 表格）：
      [0] 項次  [1] 機關名稱  [2] 標案案號  [3] 招購代碼(跳過)
      [4] 招標方式  [5] 採購類別(跳過)  [6] 公告日期
      [7] 截止投標日期  [8] 預算金額  [9] 功能(跳過)

    標案名稱藏在每列的 <script> 標籤中（pageCode2Img 防爬機制），用 regex 提取。
    """
    soup = BeautifulSoup(html, "html.parser")
    bids: List[Dict] = []

    table = soup.find("table", {"class": "tb_01"})
    if table is None:
        for t in soup.find_all("table"):
            if len(t.find_all("tr")) > 1:
                table = t
                break

    if table is None:
        return []

    data_rows = [r for r in table.find_all("tr") if r.find("td")]

    for i, row in enumerate(data_rows, start=1):
        cells = row.find_all("td")
        if len(cells) < 9:
            continue
        bids.append({
            "index": i,
            "agency": cells[1].get_text(strip=True),
            "bid_number": cells[2].get_text(strip=True),
            "bid_name": _extract_bid_name(row),                  # 從 <script> 提取
            "procurement_method": cells[4].get_text(strip=True),
            "announcement_date": cells[6].get_text(strip=True),
            "deadline": cells[7].get_text(strip=True),
            "budget": cells[8].get_text(strip=True),
        })

    return bids


def scrape_all() -> List[Dict]:
    """
    爬取勞務類 842 等標期內全部標案（自動翻頁），再依關鍵字過濾標案名稱。
    若某頁回傳筆數小於 pageSize，代表已是最後一頁。
    """
    session = requests.Session()
    session.get(INDEX_URL, headers=HEADERS, timeout=30)

    all_bids: List[Dict] = []
    page = 1
    page_size = 100

    while True:
        html = fetch_page(session, page=page)
        bids = parse_bids(html)
        all_bids.extend(bids)

        if len(bids) < page_size:
            break

        page += 1
        time.sleep(random.uniform(0.5, 1.5))

    filtered = [
        bid for bid in all_bids
        if any(kw in bid["bid_name"] for kw in KEYWORDS)
    ]

    for i, bid in enumerate(filtered, start=1):
        bid["index"] = i

    return filtered
