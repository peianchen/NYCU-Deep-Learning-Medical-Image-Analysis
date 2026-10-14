"""Extract candidate figures locally and build contact sheets for review."""

import argparse
import base64
import json
import re
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw

from course_config import COURSE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--student-id", required=True)
    args = parser.parse_args()
    root = args.source
    local = Path(".local/figures")
    local.mkdir(parents=True, exist_ok=True)
    records = []
    for folder, pattern, name, title in COURSE:
        path = root / pattern.format(student=args.student_id)
        notebook = json.loads(path.read_text(encoding="utf-8-sig"))
        for index, cell in enumerate(notebook["cells"]):
            for output_index, output in enumerate(cell.get("outputs", [])):
                encoded = output.get("data", {}).get("image/png")
                if encoded:
                    key = f"{folder}__{Path(name).stem}__cell{index:02d}__out{output_index:02d}.png"
                    (local / key).write_bytes(base64.b64decode("".join(encoded)))
                    records.append({"key": key, "folder": folder, "notebook": name, "cell": index, "output": output_index})
    for hw in sorted(root.glob("hw*")):
        for document in sorted(hw.rglob("*.docx")):
            if "ans" in document.parts:
                continue
            with ZipFile(document) as archive:
                for entry in archive.namelist():
                    if entry.startswith("word/media/") and entry.lower().endswith((".png", ".jpg", ".jpeg")):
                        number = re.search(r"\d+", Path(entry).stem).group()
                        part = "p2" if "HW3_2" in document.name else "p1" if "HW3_1" in document.name else "report"
                        key = f"{hw.name}__{part}__image{int(number):02d}{Path(entry).suffix.lower()}"
                        (local / key).write_bytes(archive.read(entry))
                        records.append({"key": key, "folder": hw.name, "document": document.name})
    records.sort(key=lambda item: item["key"])
    (local / "candidates.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    for start in range(0, len(records), 12):
        sheet = Image.new("RGB", (1800, 4 * 320), "#eeeeee")
        draw = ImageDraw.Draw(sheet)
        for offset, record in enumerate(records[start:start+12]):
            image = Image.open(local / record["key"]).convert("RGB")
            image.thumbnail((590, 270))
            x, y = (offset % 3) * 600, (offset // 3) * 320
            sheet.paste(image, (x + (600-image.width)//2, y))
            draw.text((x+8, y+274), record["key"].replace("__", "\n"), fill="black")
        sheet.save(local / f"contact-{start//12+1:02d}.jpg")
    print(f"{len(records)} candidate figures; {(len(records)+11)//12} contact sheets. None copied into public assets.")


if __name__ == "__main__":
    main()
