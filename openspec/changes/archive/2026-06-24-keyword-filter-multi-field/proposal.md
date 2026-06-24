## Why

目前「醫院」排除按鈕只檢查標案名稱（`bid_name`），但機關名稱（`agency`）為醫院的標案同樣不屬於接案公司目標客群，需要一併排除。同時，為了讓其他關鍵字未來也能靈活指定排除欄位，改以設定表取代硬編碼邏輯。

## What Changes

- 將前端關鍵字定義從字串陣列改為**設定物件陣列**，每個關鍵字可指定要比對的欄位（`fields`）
- 「醫院」關鍵字排除範圍擴展為 `bid_name`（標案名稱）**及** `agency`（機關名稱），只要任一欄位命中即排除
- 其餘三個關鍵字（設備、機房、儀器）維持只比對 `bid_name`
- UI 不變（仍為四顆按鈕，使用者體驗無差異）

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `bid-keyword-filter`：排除邏輯由「只比對 bid_name」改為「依各關鍵字的 fields 設定比對對應欄位」，「醫院」同時比對 bid_name 與 agency

## Impact

- **前端**：`frontend/src/App.jsx` — `KEYWORDS` 常數結構調整、`filteredBids` 篩選邏輯更新
- **後端**：無需修改
- **依賴套件**：無新增
