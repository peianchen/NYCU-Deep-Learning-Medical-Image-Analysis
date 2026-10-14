# NYCU Deep Learning in Medical Image Analysis

深度學習於醫學影像分析課程專案，整理五份作業的問題設定、資料處理、模型設計、歷史結果與限制。內容由課程提交 Notebook 與本人報告交叉整理，說明各影像任務的實作流程與實驗觀察。

**本專案是課程研究實作，不是臨床診斷工具。** 公開版本不包含病患影像、DICOM、個案資料表、模型權重或原始報告；Notebook 已清除全部歷史輸出與個資。結果圖只保留人工審查過的統計、學習曲線與參數／程式截圖。

## 五份作業

| 作業 | 主題與方法 | 實作內容 | 詳細入口 |
| --- | --- | --- | --- |
| HW1 | 手寫數字分類：MLP、BatchNorm、Dropout | Dataset／DataLoader、訓練迴圈、過擬合分析 | [數字分類](homeworks/hw01-digits/README.md) |
| HW2 | SPECT 三分類：VGG、ResNet、ViT、年齡／性別融合 | DICOM 切片、遷移學習、影像與表格特徵結合 | [SPECT 分類](homeworks/hw02-spect/README.md) |
| HW3 | SPECT 六分類與 MRI 多切片／3D 分析 | 資料不平衡、體積前處理、架構與評估核對 | [SPECT／MRI](homeworks/hw03-spect-mri/README.md) |
| HW4 | 超音波頸動脈分割：FCN、U-Net、RLE | 像素級監督、同步增強、Dice／IoU、遮罩輸出 | [超音波分割](homeworks/hw04-segmentation/README.md) |
| HW5 | 胸腔 X 光偵測：COCO、Faster R-CNN、CAM | 多標籤分割資料、偵測訓練、AP 評估與可解釋性 | [X 光偵測](homeworks/hw05-detection/README.md) |

每份作業包含詳細 `README.md`、程式／函式索引 `FILES.md`、公開證據索引 `RESULTS.md`。HW3 與 HW5 另有各子題說明。可從 [專案概覽](docs/PROJECT_OVERVIEW.md) 了解整體流程，再依感興趣的主題閱讀。

## 結果摘要

以下是**保存於原 Notebook／報告的歷史結果，不是本次重新訓練**，也不是 Kaggle 私有測試集或外部臨床驗證分數。

| 實驗 | 歷史紀錄 | 必須一起閱讀的限制 |
| --- | --- | --- |
| HW1 MLP | 第 25 epoch validation accuracy 98.08%，macro-F1 97.87% | 不等同於最低 validation loss 所選 checkpoint 的獨立測試成績 |
| HW3 SPECT oversampling | validation accuracy 51.52%，macro-F1 21.59% | 訓練表現高但泛化與少數類別辨識不足 |
| HW3 MRI Single_slice | 保存的 checkpoint validation accuracy 93.75%，macro-F1 93.73% | 僅 16 人的 validation；此名稱實際含多切片機率平均 |
| HW4 U-Net | 最後紀錄 mean IoU 97.26%、mean Dice 98.60% | 影格隨機分割，不能視為跨受試者泛化結果 |
| HW5 Faster R-CNN | validation AP50 0.396、AP@[.50:.95] 0.222 | train-validation gap 明顯；CSV 座標輸出另有待修正問題 |

HW2 的保存輸出不足以建立完整的三模型公平排行榜；不補造缺失數字。所有結果、來源定位與規格落差見 [結果解讀](docs/RESULTS_ANALYSIS.md) 及 [歷史彙整輸出](docs/historical-metrics.json)。

## 公開內容與重現方式

```text
homeworks/   五份作業說明、八份清除輸出的 Notebook、已審查圖表
docs/        專案概覽、環境、資料政策、結果分析、驗證與來源雜湊
tools/       原始資料只讀匯入、去識別整理、圖片審查與驗證工具
```

模型流程依賴課程授權資料、外部 pretrained weights 與原套件環境，**不是 clone 後即可直接 Run All 的專案**。請先閱讀 [環境與執行](docs/ENVIRONMENT.md)、各作業的資料目錄與已知問題，再準備有權使用的資料。

本次檢查日期為 2026-10-14。檢查內容包含 Notebook 格式、Python 靜態語法、來源雜湊、文件連結、圖片完整性與無醫學資料的 RLE 測例；沒有執行 GPU 訓練、完整推論或臨床驗證。[驗證紀錄](docs/VERIFICATION.md) 將實際檢查範圍單獨列出。

八份 Notebook 的 228 個 code cells、十二份 Python 檔案通過語法檢查。RLE 在目前 NumPy 2 下，原版六例僅一例通過；新增的獨立相容字串函式搭配原 encode／decode 六例全通過，未修改原 Notebook，也不以相容版結果掩蓋原版限制。

## 使用與來源

作業是基於課程 scaffold、常用模型與本人提交版本延伸，不宣稱整套框架或預訓練模型皆為自行從零開發。HW5 的 Torchvision detection helpers 保留 [第三方來源說明](homeworks/hw05-detection/notebooks/THIRD_PARTY.md) 與原授權。MedicalNet、CAM 等外部程式不打包進本 repository。

[資料與隱私政策](docs/DATA_POLICY.md) · [程式來源雜湊](docs/source-manifest.json) · [課程索引](docs/HOMEWORKS.md) · [工具說明](tools/README.md)
