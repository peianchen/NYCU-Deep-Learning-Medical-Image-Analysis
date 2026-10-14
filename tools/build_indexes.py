"""Generate navigable per-homework figure and notebook indexes."""

import ast
import json
from collections import defaultdict
from pathlib import Path

from course_config import COURSE


def main():
    figures = json.loads(Path("docs/figures.json").read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for folder, _, filename, title in COURSE:
        groups[folder].append((filename, title))
    overview = ["# 課程與程式導覽", "", "[首頁](../README.md) · [面試閱讀](INTERVIEW_GUIDE.md)", "", "| 作業目錄 | 主要程式 | 公開結果圖 |", "| --- | --- | --- |"]
    for folder, entries in groups.items():
        root = Path("homeworks") / folder
        records = [item for item in figures if item["destination"].startswith(root.as_posix() + "/")]
        inventory = ["# 程式與函式索引", "", "[作業說明](README.md) · [公開結果圖](RESULTS.md)", "", "Notebook 為去識別提交副本，不是可直接 Run All 的完成產品；資料、權重與完整原環境不公開。保留 source-NNN cell ID 方便與歷史彙整輸出對應。", "", "| Notebook | 主要用途 |", "| --- | --- |"]
        for filename, title in entries:
            inventory.append(f"| [{filename}](notebooks/{filename}) | {title} |")
        for filename, title in entries:
            inventory.extend(["", f"## {filename}", "", title, ""])
            notebook = json.loads((root / "notebooks" / filename).read_text(encoding="utf-8"))
            for cell in notebook["cells"]:
                if cell["cell_type"] != "code":
                    continue
                try:
                    nodes = ast.parse("".join(cell["source"])).body
                except SyntaxError:
                    inventory.append(f"- `{cell['id']}`：保留原碼語法問題，詳見 verification.json。")
                    continue
                definitions = [f"{type(node).__name__}: {node.name}" for node in nodes if isinstance(node, (ast.ClassDef, ast.FunctionDef))]
                if definitions:
                    inventory.append(f"- `{cell['id']}`：" + "；".join(f"`{value}`" for value in definitions))
        helpers = sorted((root / "notebooks").glob("*.py"))
        if helpers:
            inventory.extend(["", "## 偵測 helpers", "", "這些是課程沿用的 Torchvision reference helpers，非自行從零開發，來源與授權見 [THIRD_PARTY](notebooks/THIRD_PARTY.md)。", ""])
            for helper in helpers:
                inventory.append(f"- [{helper.name}](notebooks/{helper.name})")
        (root / "FILES.md").write_text("\n".join(inventory) + "\n", encoding="utf-8", newline="\n")
        gallery = ["# 公開結果證據", "", "[作業說明](README.md) · [程式索引](FILES.md)", "", f"共 {len(records)} 張經審查的歷史圖表／截圖。全部來自原 Notebook 或本人 Word 報告，不是本次重訓產生；不包含病患影像、遮罩或個案表。結果意義與限制請配合作業 README。", ""]
        for index, record in enumerate(records, 1):
            target = Path(record["destination"]).relative_to(root).as_posix()
            gallery.extend([f"## {index:02d} {record['caption']}", "", f"![{record['caption']}]({target})", ""])
        (root / "RESULTS.md").write_text("\n".join(gallery), encoding="utf-8", newline="\n")
        (root / "notebooks/README.md").write_text("# Notebook 閱讀入口\n\n[作業說明](../README.md) · [逐檔與 cell 索引](../FILES.md)\n\n所有歷史輸出已移除；圖表與可公開數值分別在 RESULTS 與根目錄 docs 的 historical-metrics.json。先準備有權使用的資料與可信權重、檢查已知問題，再依序執行。\n", encoding="utf-8", newline="\n")
        overview.append(f"| [{folder}](../homeworks/{folder}/README.md) | {len(entries)} Notebook | {len(records)} |")
    overview.extend(["", "HW3 含 SPECT 與 MRI 兩個子題，HW5 含前處理、CAM 與訓練三個階段。全部主題與結果皆以實際程式及本人報告核對；ans、sample、checkpoint notebooks 與重複備份不列為本人新作品。", "", "公開來源 alias 與 SHA-256 見 [source-manifest.json](source-manifest.json)，去識別政策見 [DATA_POLICY](DATA_POLICY.md)。", ""])
    Path("docs/HOMEWORKS.md").write_text("\n".join(overview), encoding="utf-8", newline="\n")
    print("Generated five homework source / evidence indexes and notebook entry pages.")


if __name__ == "__main__":
    main()
