## ADDED Requirements

### Requirement: 爬取標案按鈕
前端頁面 SHALL 提供「爬取標案」按鈕，讓使用者主動觸發後端爬蟲。

#### Scenario: 點擊按鈕觸發爬蟲
- **WHEN** 使用者點擊「爬取標案」按鈕
- **THEN** 系統 SHALL 呼叫 `POST /api/scrape`，按鈕進入 disabled 狀態並顯示「爬取中…」

#### Scenario: 爬取成功後更新畫面
- **WHEN** `POST /api/scrape` 回傳 HTTP 200
- **THEN** 系統 SHALL 將回傳的標案資料渲染至表格，並恢復按鈕可點擊狀態

#### Scenario: 爬取失敗顯示錯誤
- **WHEN** `POST /api/scrape` 回傳錯誤或網路失敗
- **THEN** 系統 SHALL 顯示錯誤訊息，並恢復按鈕可點擊狀態

### Requirement: 標案資料表格
前端 SHALL 以表格形式顯示爬取結果，包含所有規定欄位。

#### Scenario: 顯示標案清單
- **WHEN** 爬取結果回傳後
- **THEN** 系統 SHALL 渲染包含以下欄位的表格：項次、機關名稱、標案案號、標案名稱、招標方式、公告日期、截止投標日期、預算金額

#### Scenario: 無資料時顯示提示
- **WHEN** 爬取結果為空陣列
- **THEN** 系統 SHALL 在表格區域顯示「無符合條件的標案」提示

### Requirement: 下載 CSV 按鈕
前端 SHALL 提供「下載 CSV」按鈕，讓使用者將當前資料存成 CSV 檔。

#### Scenario: 成功觸發下載
- **WHEN** 使用者點擊「下載 CSV」且已有爬取資料
- **THEN** 系統 SHALL 呼叫 `GET /api/download-csv`，瀏覽器自動下載 `bids.csv`

#### Scenario: 尚無資料時停用按鈕
- **WHEN** 尚未執行爬取或爬取結果為空
- **THEN** 「下載 CSV」按鈕 SHALL 處於 disabled 狀態

### Requirement: 載入狀態顯示
前端 SHALL 在等待後端回應期間提供視覺反饋。

#### Scenario: 爬取期間顯示載入指示
- **WHEN** 爬取請求已送出、尚未收到回應
- **THEN** 系統 SHALL 顯示載入指示（spinner 或文字提示），並禁用爬取按鈕
