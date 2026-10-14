# Faster R-CNN 訓練與推論

[HW5 主說明](../README.md) · [Notebook](../notebooks/detection_training.ipynb)

此階段讀前處理產生的 COCO train／val JSON 與 JPG，建立 Dataset／collate_fn，使用 COCO pretrained Faster R-CNN ResNet50 FPN，更換七異常類別加 background 的輸出 head。

影像／BoundingBoxes 同步 resize，XYWH 轉 XYXY。以四項 loss 相加訓練，使用 COCO AP 評估，選較佳 validation AP50 的 checkpoint；歷史最末 validation AP50=0.396，不是重新測試或病患診斷 accuracy。

最後推論 score>0.5 的非 background 框並輸出 CSV。但目前 resized 512 canvas 與原 JPG W／H 的座標除法可能不一致，使用前需修正並做 synthetic bbox 測試。能寫出 CSV 不能取代座標正確性驗證。
