## Context

前端 `App.jsx` 目前的 `KEYWORDS` 常數為字串陣列：

```js
const KEYWORDS = ['設備', '機房', '醫院', '儀器']
```

篩選邏輯統一只比對 `bid_name`：

```js
bids.filter(bid => ![...activeKeywords].some(kw => bid.bid_name?.includes(kw)))
```

需求是讓「醫院」同時比對 `bid_name` 與 `agency`，同時保留未來擴充其他欄位的彈性。

## Goals / Non-Goals

**Goals:**
- 將 `KEYWORDS` 改為設定物件陣列，每個關鍵字附帶 `fields` 陣列指定要比對的欄位
- 「醫院」預設比對 `['bid_name', 'agency']`，其餘三個維持 `['bid_name']`
- 篩選邏輯改讀 `fields` 設定，不再硬編碼欄位名稱
- UI 及使用者操作流程完全不變

**Non-Goals:**
- 讓使用者在 UI 上自行選擇要比對哪個欄位
- 修改後端邏輯

## Decisions

### 1. 設定物件結構

```js
const KEYWORDS = [
  { label: '設備', fields: ['bid_name'] },
  { label: '機房', fields: ['bid_name'] },
  { label: '醫院', fields: ['bid_name', 'agency'] },
  { label: '儀器', fields: ['bid_name'] },
]
```

- `label`：顯示在按鈕上的文字，也作為 `activeKeywords` Set 的 key
- `fields`：排除時要比對的欄位名稱陣列（對應 bid 物件的 key）

### 2. 篩選邏輯更新

原本：

```js
bids.filter(bid => ![...activeKeywords].some(kw => bid.bid_name?.includes(kw)))
```

改為：

```js
bids.filter(bid =>
  ![...activeKeywords].some(kw => {
    const config = KEYWORDS.find(k => k.label === kw)
    return config.fields.some(field => bid[field]?.includes(kw))
  })
)
```

邏輯：某列只要「任一啟用關鍵字」在「該關鍵字設定的任一欄位」中命中，即排除。

### 3. activeKeywords 仍用 label 作 key

Set 內儲存的是 `label`（字串），不需改動 `toggleKeyword` 或按鈕渲染邏輯，影響範圍最小。

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|---------|
| `KEYWORDS.find` 在每列都執行一次 | 資料量（數十至數百筆）遠低於效能門檻，可接受 |
| 未來新增欄位時需確認 bid 物件確實有該 key | `bid[field]?.includes` 已用可選鏈，欄位不存在時安全回傳 `undefined`（falsy），不會報錯 |
