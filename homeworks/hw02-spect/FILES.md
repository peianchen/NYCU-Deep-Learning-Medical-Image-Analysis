# 程式與函式索引

[作業說明](README.md) · [公開結果圖](RESULTS.md)

Notebook 為去識別提交副本，不是可直接 Run All 的完成產品；資料、權重與完整原環境不公開。保留 source-NNN cell ID 方便與歷史彙整輸出對應。

| Notebook | 主要用途 |
| --- | --- |
| [spect_classification.ipynb](notebooks/spect_classification.ipynb) | SPECT 三分類 |

## spect_classification.ipynb

SPECT 三分類

- `source-005`：`ClassDef: config`
- `source-010`：`FunctionDef: seed_everything`；`FunctionDef: evaluator`；`FunctionDef: train_one_epoch`；`FunctionDef: validation`
- `source-012`：`ClassDef: Normalization`；`FunctionDef: build_transform`
- `source-014`：`ClassDef: ParkinsonsDataset`
- `source-017`：`ClassDef: VGGplus`
- `source-043`：`FunctionDef: main`
- `source-044`：`FunctionDef: testing`
- `source-048`：`ClassDef: ResNetplus`
- `source-053`：`FunctionDef: main`
- `source-055`：`FunctionDef: testing`
- `source-059`：`ClassDef: Normalization`；`FunctionDef: build_transform_ViT`
- `source-060`：`ClassDef: VisionTransformerCustom`
- `source-065`：`FunctionDef: main`
- `source-067`：`FunctionDef: testing`
