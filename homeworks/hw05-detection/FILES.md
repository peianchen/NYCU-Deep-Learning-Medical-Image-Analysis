# 程式與函式索引

[作業說明](README.md) · [公開結果圖](RESULTS.md)

Notebook 為去識別提交副本，不是可直接 Run All 的完成產品；資料、權重與完整原環境不公開。保留 source-NNN cell ID 方便與歷史彙整輸出對應。

| Notebook | 主要用途 |
| --- | --- |
| [preprocessing.ipynb](notebooks/preprocessing.ipynb) | X 光前處理與 COCO 格式 |
| [explainability.ipynb](notebooks/explainability.ipynb) | EigenCAM 與 AblationCAM |
| [detection_training.ipynb](notebooks/detection_training.ipynb) | Faster R-CNN 訓練與推論 |

## preprocessing.ipynb

X 光前處理與 COCO 格式

- `source-002`：`ClassDef: config`
- `source-003`：`FunctionDef: seed_everything`
- `source-008`：`FunctionDef: change_to_eng_names`
- `source-011`：`FunctionDef: plot_images_and_marks`
- `source-013`：`FunctionDef: X_ray_normalization`
- `source-014`：`FunctionDef: plot_before_and_after`
- `source-016`：`FunctionDef: mask_to_bbox`
- `source-017`：`FunctionDef: plot_bbox_and_mark`
- `source-019`：`FunctionDef: write_bbox`
- `source-022`：`FunctionDef: write_class_id`
- `source-032`：`FunctionDef: coco_format`
- `source-038`：`FunctionDef: dcm_to_jpg`
- `source-042`：`FunctionDef: dcm_to_jpg`

## explainability.ipynb

EigenCAM 與 AblationCAM

- `source-003`：`ClassDef: config`
- `source-005`：`FunctionDef: seed_everything`
- `source-006`：`FunctionDef: fasterrcnn`
- `source-007`：`FunctionDef: predict`；`FunctionDef: draw_boxes`
- `source-008`：`FunctionDef: get_transform`
- `source-010`：`FunctionDef: plot_eigen_cam_images`
- `source-011`：`FunctionDef: plot_ablation_cam_images`

## detection_training.ipynb

Faster R-CNN 訓練與推論

- `source-004`：`ClassDef: config`
- `source-005`：`FunctionDef: seed_everything`
- `source-015`：`ClassDef: medTransform`
- `source-017`：`ClassDef: MedDataset`
- `source-019`：`FunctionDef: collate_fn`
- `source-020`：`FunctionDef: plot_image_with_boxes`
- `source-025`：`FunctionDef: fasterrcnn`
- `source-029`：`FunctionDef: train_one_epoch`
- `source-031`：`FunctionDef: validation`
- `source-033`：`FunctionDef: seed_worker`
- `source-035`：`FunctionDef: main`
- `source-038`：`ClassDef: config`；`FunctionDef: predict`

## 偵測 helpers

這些是課程沿用的 Torchvision reference helpers，非自行從零開發，來源與授權見 [THIRD_PARTY](notebooks/THIRD_PARTY.md)。

- [coco_eval.py](notebooks/coco_eval.py)
- [coco_utils.py](notebooks/coco_utils.py)
- [engine.py](notebooks/engine.py)
- [transforms.py](notebooks/transforms.py)
- [utils.py](notebooks/utils.py)
