## 1. 前端：篩選狀態管理

- [x] 1.1 在 `frontend/src/App.jsx` 新增 `activeKeywords` state（`useState`，型別為 `Set` 或 `string[]`），初始值為空集合
- [x] 1.2 實作 `toggleKeyword(keyword)` 函式：若 keyword 已在 activeKeywords 中則移除，否則加入
- [x] 1.3 實作 `filteredBids` 計算邏輯：當 `activeKeywords` 為空時回傳全部 bids；否則回傳標案名稱符合任一關鍵字的資料列（OR 邏輯）

## 2. 前端：篩選按鈕 UI

- [x] 2.1 在 `App.jsx` 的爬取按鈕與表格之間，新增四個關鍵字篩選按鈕（設備、機房、醫院、儀器）
- [x] 2.2 按鈕樣式依啟用狀態切換（啟用時有視覺區別，例如背景色或 border 變化）
- [x] 2.3 每個按鈕的 `onClick` 呼叫 `toggleKeyword(keyword)`

## 3. 前端：表格與 CSV 調整

- [x] 3.1 將 `BidsTable.jsx`（或表格渲染處）的資料來源從原始 `bids` 改為 `filteredBids`
- [x] 3.2 確認「無符合條件的標案」提示在 `filteredBids` 為空時正常顯示
- [x] 3.3 將「下載 CSV」的資料來源改為 `filteredBids`，確保下載的是篩選後的結果（若 CSV 目前由後端產生，需改為前端直接用 Blob 產生並觸發下載）

## 4. 驗收測試

- [ ] 4.1 爬取資料後，點擊「設備」按鈕確認只顯示標案名稱含「設備」的列
- [ ] 4.2 同時啟用「設備」與「機房」，確認顯示命中任一關鍵字的列
- [ ] 4.3 再次點擊啟用中的按鈕，確認取消篩選、顯示正確更新
- [ ] 4.4 全部按鈕取消後確認顯示全部資料
- [ ] 4.5 在篩選狀態下點擊「下載 CSV」，確認下載的 CSV 只含篩選後的列
