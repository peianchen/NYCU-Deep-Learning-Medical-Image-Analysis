# HW4 超音波頸動脈語義分割

[課程首頁](../../README.md) · [程式索引](FILES.md) · [公開證據](RESULTS.md)

## 問題與目的

對超音波影像逐像素預測頸動脈區域，從整張圖分類轉向 semantic segmentation。重點是 image／mask 同步處理、encoder-decoder、skip connection、Dice／IoU 與 RLE 編碼。

課程題目提到血流速度評估，但這份提交 Notebook 主要完成分割及遮罩輸出，**沒有保留可確認的血流速度計算流程**。不將題目標題當成已實作功能。

## 資料與前處理

主程式：[ultrasound_segmentation.ipynb](notebooks/ultrasound_segmentation.ipynb)。原資料說明為三名志願者的影片擷取共 300 張訓練影格，測試是另一名志願者的 100 張影格。訓練 BMP 位於 `train/pre`，mask 位於 `train/post`，檔名對應為原 frame 名加 `_ROI.bmp`。

Dataset 讀取 RGB image 與二值 mask；訓練使用 Albumentations Resize、旋轉、水平翻轉、顏色／亮度變化、Normalize 與 ToTensorV2。幾何變換同時作用在 mask，避免影像轉動後標籤停留原位；validation 不使用隨機變換。

## 模型結構

| 模型 | 實際設計 | 本次保存的狀態 |
| --- | --- | --- |
| FCN | 五層卷積 block、pooling、不同尺度的 prediction 與轉置卷積相加，最後 ×8 上採樣 | 原碼有定義；不補造與 U-Net 的完整結果比較 |
| U-Net | encoder 通道 64→128→256→512→1024，decoder 上採樣並 concat 對應 skip，1×1 輸出兩類 | sweeper 主流程選用此模型 |

U-Net 的 conv block 是 Conv2d／ReLU／Conv2d／ReLU，**沒有 BatchNorm**。報告以 BatchNorm 解釋穩定訓練的敘述，不適用於這個 U-Net class；FCN 有 BatchNorm，兩者應分開。

歷史 U-Net 參數為 31,379,010。這是完整模型數量，不只是分類／分割 head。

![U-Net 參數紀錄](assets/report__image01.png)

## 訓練流程

1. 收集影格路徑，固定 seed=42，以 80／20 隨機切 train／validation。
2. 兩集合分別建立訓練與驗證 transform，再取相應索引。
3. 使用 U-Net、AdamW 與 CrossEntropyLoss 進行二類像素監督。
4. 利用 confusion matrix 累計 IoU／Dice，保存較佳 validation Dice 的 checkpoint。
5. 推論時將分割結果還原到目標尺寸，輸出 RLE 字串與 CSV。

預設 batch size=4、epochs=40、lr=1e-4、weight_decay=0，輸入 `(4,3,224,224)`，輸出遮罩目標尺寸 `(566,640)`。Notebook 雖印出 `Use Cosine LR scheduler`，未見相應 scheduler 建立／step，不能只依印出的字串宣稱有 cosine 排程。

W&B 有 logger／sweep 介面，預設不啟用 wandb。使用者若要啟用，必須自行設定帳戶，不應上傳病患影像、個案資訊或存取憑證。

## 歷史結果與評估解讀

最後保存的驗證輸出：

| 指標 | 背景 | 頸動脈前景 | 平均 |
| --- | --- | --- | --- |
| IoU | 約 99.2% | 約 95.3% | 97.26% |
| Dice | 約 99.62% | 約 97.59% | 98.60% |

mean 指標同時含背景；討論實際目標品質時，應特別看前景結果。這是當時 frame-level validation，不是本次重新推論，也不是跨病患／醫院的臨床成績。

原資料訓練影格來自僅三位受試者，而原碼是隨機切影格。同一人的相近影格可能同時出現在 train／validation，使 validation 偏樂觀。後續應使用 subject/video-level split；不能用高 Dice 推論已解決 domain shift。

## RLE 與本次可獨立檢查的功能

`rle_encode` 採 column-major（先轉置再 flatten）、1-based 起點與連續長度；空遮罩用 `-`。`rle_decode` 以 Fortran order 還原，方向必須一致，否則 shape 正確也可能將遮罩轉錯。

本次不讀取醫學影像，只對人工建立的空白、全前景、單像素、矩形、棋盤及固定種子隨機 mask 重新執行 encode／decode round-trip，發現原 `list_to_string` 依賴 NumPy scalar 的 list repr；NumPy 2 會出現 `np.int64(...)`，非空遮罩無法由原解碼器轉回整數。

另附 [rle_compat.py](../../tools/rle_compat.py)，僅把字串轉換改為逐值 `int` 後串接，不修改原提交 Notebook。原函式與相容版的測試分開記錄於 [驗證文件](../../docs/VERIFICATION.md)；採用相容函式後的成功不能稱為原版也全部通過。這仍不等於重新驗證模型分割能力。

## 如何執行與限制

依 [環境說明](../../docs/ENVIRONMENT.md) 準備相容套件，調整 `get_args` 的 root／data_path／output_dir，並確認 image／mask 配對。原 Kaggle 路徑不能直接假設在本機存在；未提供授權資料與權重前不應 Run All。

目前公開版不顯示超音波、個案 mask 或訓練範例疊圖。保留的圖片只有參數與增強程式截圖。後續改善包括病患分層驗證、邊界指標、FCN／U-Net 同條件比較、mask 插值策略與輸出尺寸檢查。
