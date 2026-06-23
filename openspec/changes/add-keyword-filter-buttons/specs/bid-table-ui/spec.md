## MODIFIED Requirements

### Requirement: 下載 CSV 按鈕
前端 SHALL 提供「下載 CSV」按鈕，讓使用者將**目前表格顯示的資料**存成 CSV 檔（即篩選後的資料，若無篩選則為全部資料）。

#### Scenario: 成功觸發下載（無篩選）
- **WHEN** 使用者點擊「下載 CSV」且已有爬取資料、未啟用任何關鍵字篩選
- **THEN** 系統 SHALL 下載包含全部爬取結果的 `bids.csv`

#### Scenario: 成功觸發下載（有篩選）
- **WHEN** 使用者啟用一個或多個關鍵字篩選後點擊「下載 CSV」
- **THEN** 系統 SHALL 下載僅包含目前篩選後可見資料列的 `bids.csv`

#### Scenario: 尚無資料時停用按鈕
- **WHEN** 尚未執行爬取或爬取結果為空
- **THEN** 「下載 CSV」按鈕 SHALL 處於 disabled 狀態
