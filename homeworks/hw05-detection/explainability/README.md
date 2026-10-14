# 偵測模型可解釋性

[HW5 主說明](../README.md) · [Notebook](../notebooks/explainability.ipynb)

此階段使用外部 pytorch-grad-cam 的 EigenCAM／AblationCAM、FasterRCNNBoxScoreTarget 與 FPN reshape transform，檢視同一偵測 checkpoint 的特徵關注區域。需先完成訓練與類別映射核對，不能在未訓練 task head 上解讀熱力圖為可靠模型判斷。

CAM 是模型除錯與觀察方法，不是病理定位標準或因果證據。原報告的醫學影像疊圖未公開，保留程式與方法說明即可進行技術討論；沒有宣稱醫師一致性或臨床驗證。
