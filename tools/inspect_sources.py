"""Read course documents and notebooks into ignored local audit files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfReader


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    root = args.source.resolve()
    local = Path(".local/audit")
    local.mkdir(parents=True, exist_ok=True)
    inventory = []
    for hw in sorted(root.glob("hw*")):
        for path in sorted(hw.rglob("*")):
            if not path.is_file() or any(part in {"ans", ".ipynb_checkpoints"} for part in path.relative_to(hw).parts):
                continue
            if path.suffix not in {".ipynb", ".docx", ".pdf", ".py"}:
                continue
            relative = path.relative_to(root).as_posix()
            key = relative.replace("/", "__")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if path.suffix == ".ipynb":
                notebook = json.loads(path.read_text(encoding="utf-8-sig"))
                code, output, markdown = [], [], []
                image_count = 0
                for index, cell in enumerate(notebook.get("cells", [])):
                    content = "".join(cell.get("source", []))
                    (code if cell.get("cell_type") == "code" else markdown).append(f"\n# CELL {index}\n{content}")
                    for item in cell.get("outputs", []):
                        if "text" in item:
                            output.append("".join(item["text"]))
                        data = item.get("data", {})
                        if "text/plain" in data:
                            output.append("".join(data["text/plain"]))
                        image_count += "image/png" in data
                        if item.get("output_type") == "error":
                            output.append(str(item.get("ename")) + ": " + str(item.get("evalue")))
                for suffix, lines in (("code.py", code), ("output.txt", output), ("markdown.txt", markdown)):
                    (local / f"{key}.{suffix}").write_text("\n".join(lines), encoding="utf-8")
                inventory.append({"path": relative, "sha256": digest, "cells": len(notebook.get("cells", [])), "code_cells": sum(c.get("cell_type") == "code" for c in notebook.get("cells", [])), "images": image_count, "code_lines": sum(len(x.splitlines()) for x in code)})
            elif path.suffix == ".docx":
                with ZipFile(path) as archive:
                    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                    document = ET.fromstring(archive.read("word/document.xml"))
                    text = "\n".join("".join(n.text or "" for n in p.findall(".//w:t", namespace)) for p in document.findall(".//w:p", namespace))
                    (local / f"{key}.txt").write_text(text, encoding="utf-8")
                    media_dir = local / f"{key}.media"
                    media_dir.mkdir(exist_ok=True)
                    media = sorted(entry for entry in archive.namelist() if entry.startswith("word/media/"))
                    for entry in media:
                        (media_dir / Path(entry).name).write_bytes(archive.read(entry))
                    inventory.append({"path": relative, "sha256": digest, "images": len(media)})
            elif path.suffix == ".pdf":
                if "report_example" in path.name:
                    continue
                reader = PdfReader(path)
                (local / f"{key}.txt").write_text("\n".join(page.extract_text() or "" for page in reader.pages), encoding="utf-8")
                inventory.append({"path": relative, "sha256": digest, "pages": len(reader.pages)})
            else:
                (local / f"{key}.txt").write_text(path.read_text(encoding="utf-8-sig"), encoding="utf-8")
                inventory.append({"path": relative, "sha256": digest})
    (local / "inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(inventory, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
