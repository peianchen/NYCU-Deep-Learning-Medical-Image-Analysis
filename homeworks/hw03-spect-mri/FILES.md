# 程式與函式索引

[作業說明](README.md) · [公開結果圖](RESULTS.md)

Notebook 為去識別提交副本，不是可直接 Run All 的完成產品；資料、權重與完整原環境不公開。保留 source-NNN cell ID 方便與歷史彙整輸出對應。

| Notebook | 主要用途 |
| --- | --- |
| [spect_imbalance.ipynb](notebooks/spect_imbalance.ipynb) | SPECT 六分類與資料不平衡 |
| [mri_fusion.ipynb](notebooks/mri_fusion.ipynb) | MRI 切片融合與 3D CNN |

## spect_imbalance.ipynb

SPECT 六分類與資料不平衡

- `source-020`：`ClassDef: config`
- `source-021`：`FunctionDef: seed_everything`
- `source-023`：`ClassDef: ParkinsonsDataset`
- `source-025`：`ClassDef: Normalization`；`FunctionDef: build_transform`
- `source-027`：`FunctionDef: evaluator`
- `source-029`：`FunctionDef: train_one_epoch`
- `source-031`：`FunctionDef: validation`
- `source-033`：`ClassDef: ResNet50plus`
- `source-036`：`FunctionDef: main`
- `source-037`：`FunctionDef: main`
- `source-039`：`FunctionDef: testing`

## mri_fusion.ipynb

MRI 切片融合與 3D CNN

- `source-003`：`FunctionDef: seed_everything`
- `source-008`：`ClassDef: Interpolate`
- `source-010`：`FunctionDef: build_transform`
- `source-012`：`FunctionDef: evaluator`
- `source-014`：`FunctionDef: train_one_epoch`
- `source-016`：`FunctionDef: validation`
- `source-018`：`FunctionDef: testing`
- `source-021`：`ClassDef: MRI2DDataset`
- `source-024`：`ClassDef: config`
- `source-028`：`ClassDef: Late_fusion`
- `source-035`：`FunctionDef: main`
- `source-039`：`ClassDef: config`
- `source-041`：`ClassDef: Single_slice`
- `source-046`：`FunctionDef: main`
- `source-050`：`ClassDef: config`
- `source-052`：`ClassDef: Early_fusion`
- `source-056`：`FunctionDef: main`
- `source-060`：`ClassDef: config`
- `source-061`：`ClassDef: MRI3DDataset`
- `source-065`：`FunctionDef: generate_model`
- `source-067`：`ClassDef: Resnet3d`
- `source-071`：`FunctionDef: main`
