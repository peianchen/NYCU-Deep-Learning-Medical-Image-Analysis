# HW3 SPECT 資料不平衡與 MRI 多切片分析

[課程首頁](../../README.md) · [程式索引](FILES.md) · [結果圖](RESULTS.md)

這份作業有兩個不同問題：**Problem 1 延伸 HW2 的 SPECT 六分類，Problem 2 才是 MRI 正常／腦瘤二分類**。原 Word 頁首籠統寫 MRI，這裡依題目與原碼重新對應，不將兩題混為同一資料集。

## Problem 1 六類 SPECT 與資料不平衡

入口：[spect_imbalance.ipynb](notebooks/spect_imbalance.ipynb) · [子題說明](problem01/README.md)。目的為處理原始六種 Stage_New 標籤中的少數類別，同時觀察大模型在小樣本上的過擬合。

主模型使用 ImageNet ResNet50、移除原 fc，影像特徵 2048 維與 age／gender 串接，再經 Dropout(0.5) 和 `Linear(2050,6)`。前處理沿用三相鄰 SPECT 切片、50 × 50 crop 與正規化，訓練另有旋轉／翻轉。

先以 `stratify=Stage_New` 做 80／20 分割，才對訓練部分 oversample，避免先複製資料再切分的直接洩漏。歷史紀錄為 train=128、validation=33；原 train 六類數量 `[3,14,18,33,55,5]`，oversampling 後各 55 筆，共 330 筆。

| 設定 | 提交版本 |
| --- | --- |
| seed／epochs／batch | 42／20／32 |
| learning rate／weight decay | 1e-4／5e-3 |
| oversampling 實驗 | RandomOverSampler、AdamW、StepLR(12,0.1) |
| 另一實驗 | 計算 class_weights、Adam，但 loss 仍為未加權 CrossEntropyLoss |

**不能把第二組叫作已完成的 Weighted Cross-Entropy 對照。** 程式雖計算 class_weights，沒有傳入 `CrossEntropyLoss(weight=...)`；兩實驗的 optimizer 也不同，因此更不能把分數差歸因為加權是否有效。

| 歷史 checkpoint validation | accuracy | macro-F1 |
| --- | --- | --- |
| Random Oversampling | 51.52% | 21.59% |
| 標名 weighted-loss、實際未使用 weight 的實驗 | 39.39% | 13.85% |

![Oversampling 的 train／validation accuracy](assets/spect_imbalance__cell36__out02.png)

Oversampling 使 train accuracy 達到約 95%，validation macro-F1 卻低，代表「每類筆數相等」沒有自動解決泛化。複製少數資料並不創造新病患資訊；應以每類 recall、混淆矩陣、多次分割與實際加入權重的控制實驗再評估。

## Problem 2 MRI 影像模型比較

入口：[mri_fusion.ipynb](notebooks/mri_fusion.ipynb) · [子題說明](problem02/README.md)。目的為利用同一受試者的多張 T1／T2 切片，觀察切片層級與體積模型的輸入表示、計算成本及結果。

資料規格總計 120 人的 MRI；歷史訓練流程 64 train、16 validation，另外 40 人為課程 test。先依受試者資料列切分，再建立切片集合，而不是將同一人的切片分散到不同集合。公開 repository 不包含任何受試者資料列或影像。

### MRI 前處理

1. 使用 DICOM `InstanceNumber` 排序 T1 切片，而非純字串檔名。
2. 以 Window Center／Width 計算上下界、clip 後映射到 0..255。
3. 每張切片 resize 到 256 × 256；題目參考尺寸與本實作不同，以程式為準。
4. T1、T2 及兩者平均建立三個 channel，不是 RGB 顏色。
5. Trilinear interpolation 將每人的切片深度統一為 22。
6. 2D 流程回傳 22 張三通道圖；3D 流程輸入為 `(B,3,22,256,256)`。

切片間是**空間深度**，不是時間序列。程式依同名檔讀 T2，需另外確認 T1／T2 配對與幾何對位，不能因張數一致就保證解剖位置完全對齊。

### 實際模型，而非只看名稱

| 原碼名稱 | 實際流程 | 不可誤讀的地方 |
| --- | --- | --- |
| Single_slice | 共用 VGG16 處理每張切片，分類 Softmax 後取 22 張機率平均，再取 log | 不是只看一張切片的獨立 baseline |
| Late_fusion | 共用 2D VGG16、每張壓成 512 維，串接 22 份後分類 | 特徵串接，沒有原生 3D convolution |
| Early_fusion | 同樣以 2D VGG16 處理各切片再串接 | 目前核心與 Late_fusion 相同；不是報告所稱的輸入端 3D ResNet 融合 |
| Resnet3d | MedicalNet 3D ResNet50，調整三通道與 task head | 外部 pretrained model；本次未重新載入或訓練 |

Late／Early 的分類頭為 `512*22 → 2`，只有此 Linear 層就有 22,530 個參數。報告的該數字取自 `requires_grad` 且 backbone 凍結的展示 cell；實際 main 使用 `features_grad=True`，**不能把 22,530 當成完整 fine-tuning 模型總參數**。

### 歷史 checkpoint 結果

| 原碼實驗名稱 | validation accuracy | macro-F1 | validation loss |
| --- | --- | --- | --- |
| Late_fusion | 87.50% | 87.30% | 0.2248 |
| Single_slice | 93.75% | 93.73% | 0.3811 |
| Early_fusion | 87.50% | 87.30% | 0.2248 |
| 3D ResNet | 50.00% | 49.21% | 0.6922 |

![MRI Single_slice accuracy](assets/mri_fusion__cell46__out04.png)

validation 只有 16 人，一人就改變 accuracy 6.25 個百分點。單次結果不足以宣稱某種融合架構普遍勝出；Late／Early 還不是互異架構。3D 結果低也不能直接歸因為「3D 不適合」，應先檢查初始化、排程、凍結策略、資料量與程式問題。

## 執行方式與產物

先讀 [環境](../../docs/ENVIRONMENT.md)，分別準備授權的 SPECT 資料與 MRI DICOM 目錄。SPECT 使用 `hwk02_data/train_hwk02_new.csv`；MRI 原碼預設 Kaggle 路徑，需逐段調整 root，包括 Dataset 內寫死的路徑。

MRI Notebook 分段訓練並保存各自 checkpoint，輸出 single／late／early／3D 類別 CSV。外部 MedicalNet 需從 [官方專案](https://github.com/Tencent/MedicalNet) 取得並核對相容版本與可信權重；公開副本的 shell clone 行已註解，不自動下載。

## 重要限制與改善方向

- SPECT 第二實驗的 class_weights 未接到 loss；重做時需單一變因比較。
- MRI Early／Late 核心重複，Early 測試區段還實例化 `Late_fusion`；需重構成真正互異的比較，原始缺點目前如實保留。
- 3D conv1 的 `for param ...: param=temp` 只重新綁定區域變數，沒有把權重複製進新 layer；應另外測試與修正初始化。
- MRI Dataset 先載入全部體積到記憶體，大資料下有 RAM 壓力；改成延遲載入需衡量 I/O 成本。
- 3D OneCycleLR 的 step 頻率與配置需核對；固定 seed 不保證跨硬體／套件重現。
- 目前沒有外部資料、交叉驗證、置信區間與臨床使用證據。

這份作業適合討論資料不平衡、模型命名與實際運算不一致的查核，以及「更複雜不一定更好」背後需要哪些控制實驗。
