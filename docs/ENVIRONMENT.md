# 環境與執行說明

[課程首頁](../README.md)

## 先理解重現界線

公開 repository 保存去識別程式、說明與歷史彙整結果，不包含授權資料、模型 checkpoint 或完整原環境。此次檢查只使用 Python 3.12 做格式／語法／文件檢查與無病患資料的 RLE 測例，沒有安裝完整 PyTorch 訓練環境或重新量測模型分數。

`requirements.txt` 是從實際 imports 整理的**依賴清單，不是經完整訓練驗證的 lockfile**。PyTorch／Torchvision、timm、Albumentations、pydicom 等 API 會受版本影響，應先選擇互相相容且符合原碼的環境，不能假設安裝最新套件就必然重現。

本次已確認 NumPy 2 與原 RLE list 字串格式不相容，另附可選的 tools/rle_compat.py。若重跑 HW4，需明確採用該轉換函式（或等效的逐值 int 格式）並重新測試；只讀取原 Notebook 不會自動套用此 adapter。

## 閱讀與檢查模式

只想看作品集，不需下載影像或安裝 GPU 套件：直接閱讀各作業 README、FILES、RESULTS。若要重跑文件／語法檢查，可使用獨立 Python 環境：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tools/requirements.txt
.\.venv\Scripts\python.exe tools/build_indexes.py
.\.venv\Scripts\python.exe tools/verify_portfolio.py --checked-on 2026-10-14
```

執行時應將 checked-on 改為當次日期。工具重寫 `docs/verification.json`，但不執行訓練 cells，也不讀取任何醫學資料或模型 pickle。

## 訓練模式的資料契約

| 作業 | 本機需準備的內容 | 路徑設定 |
| --- | --- | --- |
| HW1 | zip.train.csv、zip.test.csv，256 像素／數字 label | `config.root` |
| HW2 | train/test 表、DICOM、Age／Gender／index／Stage | `config.root`，並核對 FilePath 拼接 |
| HW3 Problem 1 | HW2 DICOM、train_hwk02_new.csv、六類 Stage_New | SPECT config.root |
| HW3 Problem 2 | train/test/submission 表、每人 T1／T2 DICOM、可信 MedicalNet 權重 | 各 config.root 及 Dataset／generate_model 內部路徑 |
| HW4 | train/pre BMP、train/post ROI masks、test/pre | get_args root／data_path／output_dir |
| HW5 | train/test 表、DICOM／mark、前處理後 JPG 與 COCO train/val JSON | 三份 Notebook 的 root、info_root、save_root 等 |

這張表只描述 schema，不提供個案資料。必須使用自己已獲授權的資料；此 repository 不重新授予課程資料的權利。

## 執行順序與注意事項

1. 先讀作業 README 的已知問題，例如 HW3 未接上的 weighted loss、重複融合架構與 HW5 座標系。
2. 在獨立環境安裝適用版本的依賴。不要為了閱讀作品集而變動既有研究／正式環境。
3. 只載入可信來源的 checkpoint；不要以 torch.load 讀取陌生檔案來試驗。
4. 調整原碼的本機／Kaggle 路徑、資料欄位、label 與尺寸契約。
5. 逐 cell 執行，不直接 Run All；多個 main／config 定義會依序覆蓋。
6. HW5 先 preprocessing，再 training；explainability 需與訓練 checkpoint、類別 mapping 一致。從 notebooks 目錄啟動 kernel，使同目錄 helpers 可被 import。
7. 將產物放在獨立、忽略的 data／outputs／checkpoints 目錄；勿將輸出、醫學圖或 credentials commit。

原 Notebook 的 `!pip`、`!git`、其他 shell／magic setup 行已註解，避免自動下載。外部 [MedicalNet](https://github.com/Tencent/MedicalNet)、[pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam) 依各自上游版本與授權使用，不打包權重。

W&B 預設不使用；若開啟需另設帳戶與限制上傳內容。原資料不會因為只傳到私人 dashboard 就自動符合公開／使用授權。

## 優先整理的工程問題

目前保留的是課程版本，不是 production pipeline。要提升可重現性，應在另行實作時統一 config、每模型獨立 train／infer 入口、明確資料 split、版本鎖定、label／bbox 契約測試及可信 checkpoint 格式；此整理沒有宣稱上述工作已全部完成。
