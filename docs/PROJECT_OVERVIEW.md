# 專案概覽

[課程首頁](../README.md) · [作業索引](HOMEWORKS.md)

本專案包含五份深度學習課程實作，從手寫數字分類開始，逐步處理 SPECT 切片、MRI 體積、超音波像素遮罩與胸腔 X 光偵測框。各作業記錄資料表示、模型、訓練流程、保存的結果及目前限制。

## 各作業在做什麼

| 作業 | 輸入與任務 | 主要處理流程 |
| --- | --- | --- |
| HW1 | 16 × 16 手寫數字，預測 0..9 | CSV → MLP → 訓練／驗證 → checkpoint → 預測類別 |
| HW2 | SPECT 切片及 age／gender，預測三類分期 | DICOM → 相鄰切片三通道 → VGG／ResNet／ViT → metadata 融合 |
| HW3 Problem 1 | SPECT 六類不平衡資料 | 分層 split → train-only oversampling → ResNet50 → macro-F1／accuracy |
| HW3 Problem 2 | T1／T2 MRI，正常／腦瘤二分類 | Windowing → resize → 22 層插值 → 2D 切片融合或 3D CNN |
| HW4 | 超音波影像與頸動脈 mask | image／mask 同步增強 → U-Net → Dice／IoU → RLE |
| HW5 | 胸腔 X 光與異常框標註 | 正規化 → subject-level split → COCO → Faster R-CNN → AP 與 CAM 分析 |

## 文件與程式的對應

每份 README 說明問題、資料需求、設計、結果與限制。FILES 列出 Notebook 與主要 class／function 所在 cell；RESULTS 保留可公開的彙整圖表。公開 Notebook 已移除輸出，安全的歷史數值另保存在 docs/historical-metrics.json，附來源 cell 編號。

HW3 的兩個子題使用不同資料；HW5 的三份 Notebook 分別負責前處理、可解釋性與訓練／推論。閱讀順序可從感興趣的作業開始，不必先下載全部資料或逐頁翻原報告。

## 結果怎麼看

分類的 accuracy 與 macro-F1、分割的 Dice／IoU、偵測的 AP 衡量不同事情，不能合併成一個通用的辨識率。歷史數字也不是這次重新訓練的結果。

例如 HW4 保存的 mean Dice 98.60% 來自影格隨機切分，不等同於跨病患表現；HW5 的 validation AP50=0.396 是偵測框的 precision-recall 指標，不是病患診斷 accuracy。詳細比較見 [結果分析](RESULTS_ANALYSIS.md)。

## 目前的實作界線

原碼保留課程版本與待改進項目，包括 HW3 class weights 未接入 loss、Early／Late 融合核心重複，以及 HW5 resize 後座標正規化的契約問題。這些分析不代表程式已完成修正。

本次已檢查 Notebook 格式、靜態語法、來源雜湊、連結與圖片；RLE 另以人工 mask 測試，並附 NumPy 2 相容字串函式。沒有重新驗證模型訓練、GPU、完整推論或臨床表現，詳見 [驗證紀錄](VERIFICATION.md)。

## 資料與執行

程式基於課程 scaffold、本人提交版本與第三方模型／工具整理。完整訓練需要有權使用的資料、可信權重、相容套件及路徑設定，不是 clone 後可直接 Run All 的產品。

醫學影像、個案表、預測清單與模型權重不公開。此處提供方法、程式與彙整結果，不包含臨床診斷使用保證。資料邊界見 [資料政策](DATA_POLICY.md)，執行需求見 [環境說明](ENVIRONMENT.md)。
