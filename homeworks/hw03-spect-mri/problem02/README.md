# Problem 2 MRI 切片與體積分類

[HW3 主說明](../README.md) · [Notebook](../notebooks/mri_fusion.ipynb)

此題將 T1、T2 與兩者平均作三通道，依 InstanceNumber 排序、windowing、resize 256 × 256，再插值成 22 層。2D 模型使用切片集合，3D 模型使用 `(B,3,22,256,256)`。

「程式名稱」與「實際方法」需要分開看：Single_slice 會平均多張切片機率，Early／Late 均是 2D 特徵串接，並非四個都完全互異。22,530 為凍結特徵時分類頭參數，不是實際 fine-tuning 的完整模型總量。

歷史 validation 僅 16 人；分數與程式問題詳見上層 README。外部 MedicalNet／可信 pretrained weights、資料對位、參數初始化與跨受試者驗證都應在重新比較前確認。
