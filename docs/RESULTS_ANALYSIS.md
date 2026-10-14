# 歷史結果的來源與解讀

[課程首頁](../README.md) · [歷史彙整資料](historical-metrics.json)

## 證據層級

原 Notebook 的保存輸出與本人報告是歷史證據，不保證與最後儲存的每一行程式完全同步。公開副本清除了完整輸出；安全的數值行另以 Notebook 路徑與原 source cell 編號保存，圖片只保留彙整曲線等允許項目。

本次沒有重新產生模型預測，也沒有替未保存的 Kaggle 分數、私人 test 標籤或缺失消融實驗補數字。指標來自不同任務、資料與 split，不建立跨作業的「最好模型」排名。

## 逐項結果

| 項目 | 歷史數字 | 正確解讀 |
| --- | --- | --- |
| HW1 最末 epoch | val acc 98.08%、macro-F1 97.87% | 第 25 epoch，不是獨立 test；best checkpoint 由 loss 選 |
| HW2 保存的部分日誌 | 30/80 epoch：val acc 69.70%、macro-F1 59.29% | 不足以認定為最後 ViT 成績或三模型完整比較 |
| HW3 oversampling | checkpoint val acc 51.52%、macro-F1 21.59% | 不平衡與泛化仍未解決，accuracy 與 macro-F1 差距大 |
| HW3 標名 weighted-loss | checkpoint val acc 39.39%、macro-F1 13.85% | 實際 loss 沒有傳入計算好的 class weights |
| MRI Late／Early | val acc 87.50%、macro-F1 87.30% | 核心架構重複，不能當作獨立 early／late 假說驗證 |
| MRI Single_slice | val acc 93.75%、macro-F1 93.73% | 實際平均 22 張切片機率；validation=16 人 |
| MRI 3D | val acc 50.00%、macro-F1 49.21% | 有初始化／排程與小資料風險，不能斷言 3D 不適合 |
| HW4 U-Net | mean IoU 97.26%、mean Dice 98.60% | 含背景、frame-level validation；非外部臨床測試 |
| HW5 detection | val AP50 .396、AP@[.50:.95] .222、AP75 .249 | 偵測 AP 非病患 accuracy，CSV 座標另有契約問題 |

## 參數數量不能混用

HW1 的 1,452,810 與 HW4 的 31,379,010 是各自模型數量。MRI 報告的 22,530 是凍結 backbone 的 Linear 頭；main 開啟 backbone fine-tuning，因此不能用這個小數字代表整個模型。HW2 的 1,864,809 是報告截圖，未在本次重新建立 timm 模型驗證。

比較模型大小時應同時記錄完整 parameters、trainable parameters、輸入尺寸、計算量及實際 peak memory。原碼以 MACs 轉 FLOPs 的印出值也需要重新統一定義，不直接當作嚴格跨模型效率比較。

## 應優先處理的評估風險

- 資料單位：同一病患多列、多切片或同一影片相近影格，應以病患／影片而非只以圖片隨機切分。
- 小樣本：MRI validation=16，單一病例影響 6.25 個 accuracy 百分點，需多次或交叉驗證與不確定性。
- 程式契約：weighted loss 是否真的使用、early／late 是否互異、resize 與 bbox 座標是否一致。
- 指標：分類看 per-class recall／macro-F1，分割看前景與邊界，偵測看 per-class AP／陰性誤報，不能只挑總體最好數值。
- 可解釋性：CAM 是模型觀察，不是 ground truth、因果證據或醫師一致性驗證。

## 後續工作而非既有成果

先修正資料／模型／輸出契約，再固定 split、記錄環境與 seed、以同條件重跑各模型，最後才比較分數。部署還需要外部資料、校正、失敗分析與臨床安全性；這些都沒有在本次文件整理中完成。
