# 程式與函式索引

[作業說明](README.md) · [公開結果圖](RESULTS.md)

Notebook 為去識別提交副本，不是可直接 Run All 的完成產品；資料、權重與完整原環境不公開。保留 source-NNN cell ID 方便與歷史彙整輸出對應。

| Notebook | 主要用途 |
| --- | --- |
| [ultrasound_segmentation.ipynb](notebooks/ultrasound_segmentation.ipynb) | 超音波頸動脈分割 |

## ultrasound_segmentation.ipynb

超音波頸動脈分割

- `source-003`：`FunctionDef: seed_everything`
- `source-004`：`FunctionDef: print_with_timestamp`
- `source-006`：`FunctionDef: rle_encode`；`FunctionDef: list_to_string`；`FunctionDef: rle_decode`
- `source-007`：`ClassDef: WandbLogger`
- `source-008`：`ClassDef: SmoothedValue`
- `source-009`：`ClassDef: MetricLogger`
- `source-011`：`FunctionDef: build_transform`
- `source-012`：`ClassDef: DeepMedical`；`ClassDef: SonoDataset`
- `source-013`：`ClassDef: config`
- `source-015`：`ClassDef: FCN`
- `source-016`：`ClassDef: UNet`
- `source-019`：`ClassDef: ConfusionMatrix`；`ClassDef: intersection_over_union`；`FunctionDef: visualization`
- `source-021`：`FunctionDef: train_one_epoch`；`FunctionDef: evaluate`
- `source-023`：`FunctionDef: get_args`
- `source-024`：`FunctionDef: sweeper`
- `source-026`：`ClassDef: SonoInferenceDataset`；`FunctionDef: inference`
