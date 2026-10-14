# X 光前處理與資料分割

[HW5 主說明](../README.md) · [Notebook](../notebooks/preprocessing.ipynb)

此階段讀 DICOM，依 Window Center／Width clip，做 log transformation 與 percentile balance，再轉成本機 JPG。標註圖由 connected components 轉 bbox，接著以 unique ID 的多標籤分布切 train／validation，輸出 COCO JSON。

輸入 schema 為 ID、category、Width、Height、Filename、ImagePath、MarkPath。相同 ID 可能多列，不應把 451 列直接當成 451 位獨立受試者。此處只描述欄位，沒有上傳任何實際資料列。

原碼只保留面積 >=3000 的第一個 connected region，且 vmin／vmax 實際改以 5／95 percentiles 計算。重新使用前應驗證多框、空框、小病灶與 class ID 映射；COCO annotations 是個案資料，仍不應公開提交 Git。
