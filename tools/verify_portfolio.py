"""Verify public artifacts without importing torch or executing training cells."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat
import numpy as np
from PIL import Image

from rle_compat import list_to_string as portable_rle_string


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def definitions(notebook: Path) -> dict:
    result = {}
    data = json.loads(notebook.read_text(encoding="utf-8"))
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            for node in ast.parse("".join(cell["source"])).body:
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    result[node.name] = node
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checked-on", required=True)
    args = parser.parse_args()
    root = Path.cwd().resolve()
    files = [p for p in root.rglob("*") if p.is_file() and not set(p.relative_to(root).parts).intersection({".local", ".planning", ".git", "__pycache__"})]
    errors, notebook_checks, python_checks = [], [], []
    link_count = 0
    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.suffix in {".dcm", ".nii", ".gz", ".pth", ".pt", ".ckpt", ".zip", ".tar", ".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".html", ".mp4", ".bmp"}:
            errors.append("Forbidden public artifact: " + relative)
        if path.suffix in {".md", ".py", ".ipynb", ".json"}:
            text = path.read_text(encoding="utf-8")
            if re.search(r"TDR\d+_\d{8}_\d+|\b[34]\d{8}\b|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-proj-[A-Za-z0-9_-]{20,}", text):
                errors.append("Potential identifier or credential: " + relative)
        if path.suffix == ".ipynb":
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            count, syntax_errors = 0, []
            for cell in notebook.cells:
                if cell.cell_type == "code":
                    count += 1
                    if cell.outputs or cell.execution_count is not None:
                        errors.append("Notebook output remains: " + relative)
                    try:
                        compile(cell.source, relative + ":" + cell.id, "exec")
                    except SyntaxError as error:
                        syntax_errors.append({"cell": cell.id, "message": str(error)})
                if "attachments" in cell:
                    errors.append("Notebook attachment remains: " + relative)
            if syntax_errors:
                errors.append("Notebook syntax failure: " + relative)
            notebook_checks.append({"path": relative, "code_cells": count, "schema_valid": True, "syntax_errors": syntax_errors, "outputs_removed": True})
        if path.suffix == ".py":
            try:
                compile(path.read_text(encoding="utf-8"), relative, "exec")
                python_checks.append({"path": relative, "syntax_valid": True})
            except SyntaxError as error:
                errors.append(f"Python syntax failure: {relative}: {error}")
        if path.suffix == ".md":
            for target in re.findall(r"!?\[[^\]\n]*\]\(([^\n)]+)\)", path.read_text(encoding="utf-8")):
                target = target.strip().strip("<>")
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                resolved = (path.parent / unquote(target.split("#")[0])).resolve()
                link_count += 1
                if not resolved.is_relative_to(root) or not resolved.exists():
                    errors.append(f"Broken link: {relative} -> {target}")
    manifest = json.loads(Path("docs/source-manifest.json").read_text(encoding="utf-8"))
    for record in manifest:
        if sha(Path(record["destination"])) != record["published_sha256"]:
            errors.append("Source hash changed: " + record["destination"])
    figures = json.loads(Path("docs/figures.json").read_text(encoding="utf-8"))
    approved = {record["destination"] for record in figures}
    for record in figures:
        path = Path(record["destination"])
        with Image.open(path) as picture:
            picture.verify()
        if sha(path) != record["sha256"]:
            errors.append("Figure hash changed: " + str(path))
    actual = {p.relative_to(root).as_posix() for p in files if p.suffix in {".png", ".jpg", ".jpeg", ".svg"}}
    if actual != approved:
        errors.append("Image files differ from reviewed allowlist")

    segmentation = Path("homeworks/hw04-segmentation/notebooks/ultrasound_segmentation.ipynb")
    funcs = definitions(segmentation)
    selected = [funcs[name] for name in ("rle_encode", "list_to_string", "rle_decode")]
    # Only these reviewed pure NumPy functions are executed, never notebook cells.
    namespace = {"np": np}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "reviewed-rle-functions", "exec"), namespace)
    masks = {
        "empty": np.zeros((5, 7), dtype=np.uint8),
        "full": np.ones((5, 7), dtype=np.uint8),
        "single_pixel": np.eye(1, 35, 17, dtype=np.uint8).reshape(5, 7),
        "rectangle": np.pad(np.ones((2, 3), dtype=np.uint8), ((1, 2), (2, 2))),
        "checkerboard": (np.indices((5, 7)).sum(axis=0) % 2).astype(np.uint8),
        "seeded_random": np.random.default_rng(42).integers(0, 2, (13, 17), dtype=np.uint8),
    }
    tests, legacy_tests = [], []
    for name, mask in masks.items():
        runs = namespace["rle_encode"](mask)
        try:
            legacy_encoded = namespace["list_to_string"](runs)
            legacy_decoded = namespace["rle_decode"](legacy_encoded, shape=mask.shape)
            legacy_tests.append({"name": name, "passed": bool(np.array_equal(mask, legacy_decoded))})
        except (ValueError, TypeError) as error:
            legacy_tests.append({"name": name, "passed": False, "error": str(error)})
        encoded = portable_rle_string(runs)
        decoded = namespace["rle_decode"](encoded, shape=mask.shape)
        passed = bool(np.array_equal(mask, decoded))
        tests.append({"name": "rle_" + name, "passed": passed, "shape": list(mask.shape)})
        if not passed:
            errors.append("RLE failure: " + name)
    model_defs = definitions(Path("homeworks/hw03-spect-mri/notebooks/mri_fusion.ipynb"))
    late, early = copy.deepcopy(model_defs["Late_fusion"]), copy.deepcopy(model_defs["Early_fusion"])
    late.name = early.name = "Fusion"
    fusion_same = ast.dump(late, include_attributes=False) == ast.dump(early, include_attributes=False)
    linear_widths = [256, 1024, 512, 512, 512, 256, 10]
    mlp_count = sum((a+1)*b for a, b in zip(linear_widths, linear_widths[1:])) + 2*sum(linear_widths[1:-1])
    checks = [
        {"name": "MLP_parameter_arithmetic_not_torch_execution", "passed": mlp_count == 1452810, "parameters": mlp_count},
        {"name": "MRI_fusion_architecture_comparison", "observation": "normalized class AST identical" if fusion_same else "AST differs; see manual core-flow review", "normalized_ast_identical": fusion_same},
    ]
    report = {
        "checked_on": args.checked_on,
        "python": sys.version.split()[0],
        "nbformat": nbformat.__version__,
        "numpy": np.__version__,
        "notebooks": notebook_checks,
        "python_files": python_checks,
        "synthetic_tests": tests,
        "synthetic_test_scope": "original encode/decode with optional tools/rle_compat.py string adapter",
        "legacy_rle_tests": legacy_tests,
        "static_observations": checks,
        "summary": {"notebooks": len(notebook_checks), "code_cells": sum(x["code_cells"] for x in notebook_checks), "python_files": len(python_checks), "approved_figures": len(figures), "local_links": link_count, "source_files_hashed": len(manifest), "compat_rle_passed": sum(x["passed"] for x in tests), "legacy_rle_passed": sum(x["passed"] for x in legacy_tests), "rle_cases": len(tests), "training_rerun": False, "integrity_errors": len(errors)},
        "errors": errors,
    }
    Path("docs/verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report["summary"], indent=2))
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
