# Problem 1 SPECT 六分類

[HW3 主說明](../README.md) · [Notebook](../notebooks/spect_imbalance.ipynb)

此題延伸 SPECT 而非 MRI。重點是六類 Stage_New、ResNet50 與訓練資料的 Random Oversampling；先分割再重採樣。少數類別重複之後，樣本數增加不等於增加獨立病患資訊。

Notebook 第一組實驗為 oversampling，第二組雖標記 weighted loss，實際沒有把 class_weights 傳進 CrossEntropyLoss。歷史 checkpoint 的 accuracy／macro-F1 分別為 51.52%／21.59% 與 39.39%／13.85%；不能稱為嚴謹的兩種 imbalance 方法優劣比較。

閱讀順序建議為類別統計、分割、重採樣、Dataset、ResNet50plus、兩個 main 與 testing。具體超參數、圖片與改善事項統一列於上層 README，避免子題出現不同版本數字。
