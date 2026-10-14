# 整理與驗證工具

[課程首頁](../README.md)

| 工具 | 用途 |
| --- | --- |
| inspect_sources.py | 只讀原文件，將 Notebook code／output 與 Word／PDF 文字抽到忽略的 .local |
| review_figures.py | 將候選圖片抽到本機並建立 contact sheets，不直接公開 |
| prepare_portfolio.py | 明確 allowlist 匯入八份提交 Notebook、清除輸出／個資、匯入五份 helpers 與 37 張審查圖 |
| build_indexes.py | 依 Notebook AST 與圖表清單建立五份 FILES／RESULTS 等索引 |
| verify_portfolio.py | Notebook schema／語法、Python 語法、雜湊、連結、圖片 allowlist、六組 synthetic RLE |
| rle_compat.py | 可選的 NumPy 2 相容字串轉換；與原 Notebook 的結果分開驗證 |

只讀／抽取工具需 pypdf、Pillow；正式檢查另需 nbformat、NumPy，見 tools/requirements.txt。它們不需要 torch，不執行訓練或載入 .pth。

```powershell
python tools/build_indexes.py
python tools/verify_portfolio.py --checked-on 2026-10-14
```

從原課程資料重建公開副本，需自行提供本機 root 與 student-id 參數；不在工具內硬編學號。prepare_portfolio 會覆寫對應 Notebook／來源清單，不應對已另行修改的公開程式直接重跑。先抽取候選圖並人工審查，再維護明確清單，不能將整個報告 media 目錄直接複製公開。

格式與靜態語法成功不等於相依套件可用或模型數字可重現。本次只執行經閱讀確認的純 NumPy RLE 函式及可選相容 adapter；原版在 NumPy 2 的失敗單獨記錄，其餘 cell 只 compile 不 execute。
