# 本次驗證範圍

[課程首頁](../README.md) · [機器可讀紀錄](verification.json)

## 執行日期與界線

2026-10-14 進行整理與檢查。使用 Python 3.12，Notebook 格式以 nbformat 驗證；每個 code cell 及 Python helper／工具只進行 compile 語法檢查，不 import torch、不執行訓練 Notebook、不載入權重。

完整計數、runtime 套件版本與錯誤清單以 [verification.json](verification.json) 為準。

| 項目 | 本次結果 |
| --- | --- |
| Notebook schema | 8／8 |
| code cell 靜態語法 | 228／228 |
| Python 檔案靜態語法 | 12／12，包含 helpers 與整理工具 |
| 審查圖片 | 37 張完整且與 allowlist 一致 |
| 匯入程式雜湊 | 13／13 |
| Markdown 相對連結 | 173 個有效 |
| 原 RLE、目前 NumPy 2 | 1／6，非空字串有 scalar repr 相容問題 |
| 獨立 adapter + 原 encode／decode | 6／6 |

MLP 參數以算術得到 1,452,810，未執行 PyTorch forward。MRI Early／Late 的 class AST 去除類名後完全一致，支持兩者不是不同核心架構的文件說明。

## 檢查項目

- 八份 Notebook 的 nbformat schema、cell IDs、code 語法及全部 outputs／execution_count／attachments 已移除。
- 五份課程沿用 helpers 與整理工具的 Python 語法。
- 十三份匯入程式的 source／published SHA-256；原始路徑對照只保留在本機忽略目錄。
- 三十七張公開圖片完整性及 SHA-256，所有圖片必須與人工審查 allowlist 完全一致。
- Markdown 相對連結、禁用檔案類型、部分個案／學號／credential 格式掃描。
- MLP 參數數量的獨立算術核對，以及 MRI Early／Late 類別的 AST 比較。

自動掃描不是完整去識別或所有機密資訊的形式化保證。圖片另外經六張 contact sheets 逐圖審閱，醫學像素、ID、個案 mask、CSV 截圖均排除；本機 audit 不上傳。

## Synthetic RLE 測試

只抽取已閱讀的 rle_encode、list_to_string、rle_decode 三個純 NumPy 函式，在人工建立的空白、全前景、單像素、矩形、棋盤、seed=42 隨機 mask 上做 encode／decode round-trip，逐元素比較原遮罩與還原遮罩。

目前 NumPy 2 下，原 list_to_string 的 list repr 會帶入 `np.int64(...)`，非空案例在 decode 轉 int 時失敗。另新增 tools/rle_compat.py 作為可選相容函式，逐值 int 後轉字串，搭配原 encode／decode 重測。原函式的結果保留在 legacy_rle_tests，相容版在 synthetic_tests；不能把兩者混為「原碼全部成功」。Notebook 原函式未改動。

這六組測試不使用任何醫學資料。它們驗證的是指定合法輸入的序列化一致性，不是 U-Net 分割準確度，也未涵蓋任意惡意／錯誤 RLE 格式。

## 沒有做的事情

沒有重新訓練 MLP／CNN／Transformer／U-Net／Faster R-CNN，沒有驗證 GPU、模型 forward、所有套件相容性、DICOM decoding、資料 split 實際內容、完整 CSV 幾何正確性、Kaggle 分數或臨床表現。

原碼已知問題沒有為了通過整理檢查而偷偷修改。尤其 weighted loss 未接上、MRI 架構命名與參數量、HW5 bbox 座標等均在 README 明列。語法檢查成功不表示這些問題消失。

## 重跑

```powershell
python tools/build_indexes.py
python tools/verify_portfolio.py --checked-on 2026-10-14
```

日期請改成當次日期；這會更新 verification.json。需要授權資料的模型驗證應另外設計，不與本檢查的成功率混為一談。
