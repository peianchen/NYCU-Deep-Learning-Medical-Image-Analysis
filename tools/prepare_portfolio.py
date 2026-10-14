"""Import an explicit code allowlist and visually reviewed aggregate figures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from course_config import COURSE


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sanitize(text: str, student: str) -> str:
    text = text.replace(student, "student")
    text = re.sub(r"TDR\d*_\d{8}_\d+", "EXAMPLE_SUBJECT", text)
    text = text.replace('default="DDCVLAB"', 'default="YOUR_WANDB_ENTITY"')
    lines = []
    for line in text.replace("\r\n", "\n").splitlines(keepends=True):
        if line.lstrip().startswith(("!", "%")):
            indent = line[:len(line)-len(line.lstrip())]
            line = indent + "# Notebook setup disabled in public copy: " + line.lstrip()
        lines.append(line)
    return "".join(lines)


def figures() -> list[tuple[str, str, str]]:
    result = [("hw1__report__image01.png", "hw01-digits", "原報告的十類訓練樣本數統計")]
    for output, label in enumerate(("loss", "accuracy", "macro-F1", "misclassification"), 1):
        result.append((f"hw01-digits__digits__cell37__out{output:02d}.png", "hw01-digits", f"手寫數字歷史 {label} 曲線"))
    result.append(("hw2__report__image01.png", "hw02-spect", "報告中的 ViT 參數截圖；為歷史紀錄，未重新建立模型確認"))
    for cell, label in ((4, "完整訓練資料的六類分布"), (9, "分割後訓練部分的六類分布")):
        result.append((f"hw03-spect-mri__spect_imbalance__cell{cell:02d}__out00.png", "hw03-spect-mri", label))
    for cell, run in ((36, "Random Oversampling 實驗"), (37, "標名 weighted-loss 的實驗（原碼未將 weight 傳入 loss）")):
        for output, label in enumerate(("loss", "accuracy", "macro-F1", "misclassification"), 1):
            result.append((f"hw03-spect-mri__spect_imbalance__cell{cell:02d}__out{output:02d}.png", "hw03-spect-mri", f"{run}的歷史 {label} 曲線"))
    for cell, run in ((35, "Late_fusion"), (46, "Single_slice"), (56, "Early_fusion"), (71, "3D ResNet")):
        for output, label in enumerate(("loss", "accuracy", "macro-F1"), 2 if cell == 71 else 3):
            result.append((f"hw03-spect-mri__mri_fusion__cell{cell:02d}__out{output:02d}.png", "hw03-spect-mri", f"MRI {run} 歷史 {label} 曲線；名稱不保證架構互異"))
    result.extend([
        ("hw3__p2__image01.png", "hw03-spect-mri", "22,530 是凍結 backbone 時的可訓練分類頭數量，不是完整模型總量"),
        ("hw4__report__image01.png", "hw04-segmentation", "U-Net 歷史參數數量截圖"),
        ("hw4__report__image02.png", "hw04-segmentation", "超音波影像及 mask 同步增強的原程式截圖"),
    ])
    for output, label in enumerate(("AP50", "total loss", "classifier loss", "box regression loss", "RPN box loss", "objectness loss"), 61):
        result.append((f"hw05-detection__detection_training__cell36__out{output:02d}.png", "hw05-detection", f"Faster R-CNN 歷史 {label} 曲線；原圖 Testing 字樣實為驗證集"))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--student-id", required=True)
    args = parser.parse_args()
    missing = [key for key, _, _ in figures() if not (Path(".local/figures") / key).is_file()]
    if missing:
        raise FileNotFoundError("Reviewed figure selection does not exist: " + ", ".join(missing))
    manifest, private, evidence = [], [], []
    for folder, pattern, filename, title in COURSE:
        source = args.source / pattern.format(student=args.student_id)
        original = source.read_bytes()
        notebook = json.loads(original.decode("utf-8-sig"))
        target = Path("homeworks") / folder / "notebooks" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        cells = [{"cell_type": "markdown", "metadata": {}, "id": "portfolio-notice", "source": [f"# {title}\n", "\n", "課程提交版本的公開整理副本。所有歷史輸出、附件及非必要 metadata 已移除。\n", "先閱讀上層 README 的資料需求、已知問題與重現限制；不要直接 Run All。\n"]}]
        for index, cell in enumerate(notebook["cells"]):
            cell_type = cell.get("cell_type")
            text = sanitize("".join(cell.get("source", [])), args.student_id)
            cell_id = f"source-{index:03d}"
            if cell_type == "code":
                cells.append({"cell_type": "code", "metadata": {}, "id": cell_id, "source": text.splitlines(keepends=True), "execution_count": None, "outputs": []})
            elif cell_type == "markdown":
                heading = next((line for line in text.splitlines() if re.match(r"^#{1,4} ", line)), "")
                if heading and not re.search(r"https?://|kaggle|submission|作業繳交", heading, re.IGNORECASE):
                    cells.append({"cell_type": "markdown", "metadata": {}, "id": cell_id, "source": [heading + "\n"]})
            metrics = []
            for item in cell.get("outputs", []):
                content = "".join(item.get("text", []))
                for line in content.splitlines():
                    if re.match(r"^\s*(?:Epoch\[\d|Valid Loss:|Average Precision\s+\(AP\)|IoU:|dice:|Number of (?:training|testing) samples:|總參數量:|總可訓練參數數量:)", line):
                        metrics.append(sanitize(line, args.student_id))
            if metrics:
                evidence.append({"notebook": target.as_posix(), "source_cell": index, "status": "historical_saved_output_not_rerun", "lines": metrics})
        public = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, "cells": cells}
        target.write_text(json.dumps(public, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        manifest.append({"source_role": title, "source_alias": folder + "/submitted/" + filename, "source_sha256": digest(original), "destination": target.as_posix(), "published_sha256": digest(target.read_bytes()), "changes": ["cleared outputs/counts/metadata/attachments", "removed non-heading markdown", "replaced student identifier and selected subject literal", "disabled notebook shell/magic setup lines", "placeholder W&B entity"]})
        private.append({"source": source.relative_to(args.source).as_posix(), "sha256": digest(original)})
    for filename in ("engine.py", "utils.py", "coco_utils.py", "coco_eval.py", "transforms.py"):
        source = args.source / "hw5" / filename
        target = Path("homeworks/hw05-detection/notebooks") / filename
        text = sanitize(source.read_text(encoding="utf-8-sig"), args.student_id)
        target.write_text("# Adapted course copy of torchvision references/detection helpers.\n# See THIRD_PARTY.md and TORCHVISION_LICENSE.txt in this directory.\n" + text, encoding="utf-8", newline="\n")
        manifest.append({"source_role": "course-provided torchvision detection helper", "source_alias": "hw5/" + filename, "source_sha256": digest(source.read_bytes()), "destination": target.as_posix(), "published_sha256": digest(target.read_bytes()), "changes": ["UTF-8/LF", "explicit third-party attribution header"]})
        private.append({"source": source.relative_to(args.source).as_posix(), "sha256": digest(source.read_bytes())})
    figure_records = []
    for key, folder, caption in figures():
        source = Path(".local/figures") / key
        target = Path("homeworks") / folder / "assets" / key.split("__", 1)[1]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        figure_records.append({"destination": target.as_posix(), "caption": caption, "status": "historical_reviewed_aggregate_figure", "sha256": digest(target.read_bytes())})
    Path("docs").mkdir(exist_ok=True)
    for name, data in (("source-manifest.json", manifest), ("historical-metrics.json", evidence), ("figures.json", figure_records)):
        (Path("docs") / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    Path(".local/original-hashes.json").write_text(json.dumps(private, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"notebooks": len(COURSE), "helpers": 5, "reviewed_public_figures": len(figure_records), "metric_cells": len(evidence)}, indent=2))


if __name__ == "__main__":
    main()
