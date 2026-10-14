# 偵測輔助程式的來源

本目錄的 `engine.py`、`utils.py`、`coco_utils.py`、`coco_eval.py`、`transforms.py` 為課程資料夾保留的 Torchvision detection reference helpers 副本／修改版，不宣稱是本人從零開發的框架。

原 Notebook 內也保留從官方 `references/detection` 下載這些檔案的註解。官方入口：[Torchvision object detection references](https://github.com/pytorch/vision/tree/main/references/detection)。原上游的精確 commit 未保存，因此不能宣稱這些本機副本與最新 main 完全相同。

各本機原始檔及公開副本的 SHA-256 記錄於 [source-manifest.json](../../../docs/source-manifest.json)。本整理只統一 UTF-8／LF 並補上歸屬標頭，不對 helper 的演算法作重寫。

Torchvision 官方 BSD 3-Clause 授權全文附於 [TORCHVISION_LICENSE.txt](TORCHVISION_LICENSE.txt)，官方授權來源為 [pytorch/vision LICENSE](https://github.com/pytorch/vision/blob/main/LICENSE)。本說明與該授權不將原醫學資料或整套課程 scaffold 重新授權。

其他外部元件，包括 [MedicalNet](https://github.com/Tencent/MedicalNet) 與 [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)，依其上游來源與授權使用；本 repository 不打包它們的程式樹或預訓練權重。
