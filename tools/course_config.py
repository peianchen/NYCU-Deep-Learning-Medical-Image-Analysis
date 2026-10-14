"""Explicit selection of the user's submitted notebooks; no dataset globbing."""

COURSE = [
    ("hw01-digits", "hw1/{student}.ipynb", "digits.ipynb", "手寫數字分類"),
    ("hw02-spect", "hw2/{student}.ipynb", "spect_classification.ipynb", "SPECT 三分類"),
    ("hw03-spect-mri", "hw3/problem_1/{student}_1.ipynb", "spect_imbalance.ipynb", "SPECT 六分類與資料不平衡"),
    ("hw03-spect-mri", "hw3/problem_2/{student}_2.ipynb", "mri_fusion.ipynb", "MRI 切片融合與 3D CNN"),
    ("hw04-segmentation", "hw4/{student}.ipynb", "ultrasound_segmentation.ipynb", "超音波頸動脈分割"),
    ("hw05-detection", "hw5/繳交檔案/{student}_1.ipynb", "preprocessing.ipynb", "X 光前處理與 COCO 格式"),
    ("hw05-detection", "hw5/繳交檔案/{student}_2.ipynb", "explainability.ipynb", "EigenCAM 與 AblationCAM"),
    ("hw05-detection", "hw5/繳交檔案/{student}_3.ipynb", "detection_training.ipynb", "Faster R-CNN 訓練與推論"),
]
