# 面試閱讀與技術討論導覽

[課程首頁](../README.md) · [作業索引](HOMEWORKS.md)

## 三分鐘看懂作品集

這個專案展示從影像分類到多切片 MRI、像素分割與物件偵測的課程實作。閱讀順序為：首頁確認範圍、選一份作業了解方法與結果，再看 Notebook 或驗證紀錄。無需先下載資料集或逐頁翻原報告。

說明重點應是「我如何處理資料、選擇模型、檢查結果及辨認限制」，而不是只背最高分數。程式基於課程 scaffold 和第三方工具延伸，應清楚交代本人整合／調整與外部框架的界線。

## 各作業可展示的內容

| 作業 | 技術主軸 | 可以深入討論的問題 |
| --- | --- | --- |
| HW1 | Dataset、MLP、訓練／驗證、checkpoint | 為何用 validation loss 選模型？Dropout 與 label smoothing 有何不同？ |
| HW2 | SPECT、遷移學習、metadata 融合 | 相鄰切片為何作三通道？凍結／微調如何取捨？age 尺度如何處理？ |
| HW3 | imbalance、MRI depth interpolation、2D／3D 表示 | 為何先 split 再 oversample？架構名稱和實際運算為何不同？小樣本比較可信嗎？ |
| HW4 | U-Net、mask 同步增強、RLE | Dice 與 IoU 衡量什麼？frame split 為何可能偏樂觀？ |
| HW5 | COCO、Faster R-CNN、AP、CAM | subject-level split、背景類別、box 座標系與熱力圖的界線 |

## 說明成果時的精確方式

可以說「原課程實驗的 U-Net frame-level validation 保存了 mean Dice 98.60%，但訓練資料來自三位受試者且採影格隨機切分，所以我不把它當成跨病患表現」。這比只說「醫學影像辨識率 98%」精確。

可以說「偵測作業整合 COCO 格式與 pretrained Faster R-CNN，保存 validation AP50=0.396，整理時也發現 resize 後座標正規化需要修正」。不要將 AP50 叫成病患 accuracy，也不要把生成 CSV 當成已證明每一框正確。

HW3 的重點不只分數：oversampling 沒解決低 macro-F1、所謂 weighted loss 未接上、Early／Late 的核心重複。能指出缺口並提出控制實驗，是對既有程式做可靠分析的一部分；不能把這些缺口描述成已經修好。

## 常見追問與回答依據

- 「這是自己從零做的嗎？」依各 README 說明自己提交的資料處理、模型修改與實驗；Torchvision／MedicalNet／CAM 與課程 scaffold 明確歸屬。
- 「我現在 clone 可以重跑嗎？」可看文件、檢查格式與 RLE；完整訓練需授權資料、可信權重、相容版本及已知問題處理。
- 「有重新驗證嗎？」本次是 Notebook 格式／語法、雜湊、連結、圖片與 synthetic RLE；未重訓，不假稱重現模型分數。
- 「原程式在新環境遇到問題怎麼辦？」用 RLE 示範：保留舊版本，重現 NumPy 2 的格式失敗，另加小型 adapter，分開記錄舊版與相容版測例，不直接把相容版成功算成舊版也正確。
- 「能用在醫院嗎？」目前只有課程實驗，沒有外部多中心、臨床安全性或法規評估，不是臨床可用產品。
- 「資料為何不放 GitHub？」醫學影像與個案識別資料的權利／隱私和程式碼不同；公開的是方法與彙整證據。

## 面試前準備

選最熟悉的一至兩份，準備從輸入到輸出的完整流程、模型維度、選 checkpoint 的指標、一個失敗案例與後續驗證設計。若未實際重新修正／訓練，應用「待改進」而不是「已改善」描述。

模型比較、完整歷史數字與已知問題分別見 [RESULTS_ANALYSIS](RESULTS_ANALYSIS.md) 與各作業 README；本次檢查見 [VERIFICATION](VERIFICATION.md)。
