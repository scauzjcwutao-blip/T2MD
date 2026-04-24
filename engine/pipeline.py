"""Conversion pipeline — automatically selects Docling or rules engine."""

import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from engine.classifier import classify, classify_content, DOCLING_EXTENSIONS, RULES_EXTENSIONS
from engine.lang import detect
from engine.rules import convert_by_rules
from engine.docling_converter import convert_by_docling

# 需要 pip install tqdm
from tqdm import tqdm


# Extensions that are binary and must go through docling (not open as text)
_BINARY_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".pptx"}


def convert(input_path: str, output_dir: str = "output") -> str:
    """
    Main conversion function.
    """
    # Step 1: Classify
    info = classify(input_path)
    ext = info["ext"].lower()
    print(f"[T2MD] File:   {info['filename']}")
    print(f"[T2MD] Format: {ext}")
    print(f"[T2MD] Engine: {info['engine']}")

    # Step 2: Convert
    if info["engine"] == "docling":
        markdown = convert_by_docling(input_path)
    else:
        if ext in _BINARY_EXTENSIONS:
            raise ValueError(
                f"Binary format '{ext}' was routed to rules engine. "
                f"Check classifier logic."
            )

        import chardet
        with open(input_path, "rb") as f:
            raw = f.read()
        encoding = chardet.detect(raw).get("encoding") or "utf-8"
        text = raw.decode(encoding, errors="replace")

        lang = detect(text)
        print(f"[T2MD] Language: {lang}")
        markdown = convert_by_rules(text, lang=lang)

    # Step 3: 内容分类 + 保存到分类子目录
    category = classify_content(markdown) if markdown.strip() else "general"
    print(f"[T2MD] Category: {category}")

    category_dir = os.path.join(output_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    base_name = os.path.splitext(info["filename"])[0]
    output_path = os.path.join(category_dir, f"{base_name}.md")

    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(category_dir, f"{base_name}_{counter}.md")
        counter += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"[T2MD] Output: {output_path}")
    return markdown


def convert_text(text: str, lang: str = "en") -> str:
    """
    Convert a text string directly (no file I/O).
    Used by GUI and tests.
    """
    return convert_by_rules(text, lang=lang)


def convert_batch(
    src_path: str,
    output_dir: str = "output",
    max_workers: int = None,
    recursive: bool = True,
) -> dict:
    """
    高效批量转换（支持10万份文件）
    """
    src = Path(src_path)
    if not src.exists():
        raise FileNotFoundError(f"Source path not found: {src_path}")

    # 收集文件
    files = []
    pattern = "**/*" if recursive and src.is_dir() else "*"
    supported = DOCLING_EXTENSIONS | RULES_EXTENSIONS

    if src.is_file():
        if src.suffix.lower() in supported:
            files = [src]
    elif src.is_dir():
        for ext in supported:
            files.extend(src.glob(f"{pattern}{ext}"))

    files = sorted(set(files))
    total = len(files)

    if total == 0:
        print("[T2MD] No supported files found.")
        return {"total": 0, "success": 0, "failed": 0, "skipped": 0}

    print(f"[T2MD] Found {total:,} files. Starting batch conversion...")

    if max_workers is None:
        max_workers = max(1, (os.cpu_count() or 4) // 2)

    success = 0
    failed = 0

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(convert, str(f), output_dir): f for f in files}

        with tqdm(total=total, desc="Converting", unit="file") as pbar:
            for future in as_completed(future_to_file):
                f = future_to_file[future]
                try:
                    future.result()
                    success += 1
                except Exception as e:
                    failed += 1
                    print(f"[T2MD] ❌ Failed {f.name}: {e}")
                pbar.update(1)

    print(f"[T2MD] Batch completed! Success: {success:,} | Failed: {failed:,}")
    return {"total": total, "success": success, "failed": failed, "skipped": 0}
