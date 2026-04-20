"""Conversion pipeline — automatically selects Docling or rules engine."""

import os
from pathlib import Path

from engine.classifier import classify
from engine.lang import detect
from engine.rules import convert_by_rules
from engine.docling_converter import convert_by_docling

# Extensions that are binary and must go through docling (not open as text)
_BINARY_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".pptx"}


def convert(input_path: str, output_dir: str = "output") -> str:
    """
    Main conversion function.

    Args:
        input_path: Path to the input file.
        output_dir: Directory for output files.

    Returns:
        Converted Markdown text.

    Raises:
        ValueError: If a binary format is routed to the rules engine.
    """
    # Step 1: Classify — decide which engine to use
    info = classify(input_path)
    ext = info["ext"].lower()
    print(f"[T2MD] File:   {info['filename']}")
    print(f"[T2MD] Format: {ext}")
    print(f"[T2MD] Engine: {info['engine']}")

    # Step 2: Convert
    if info["engine"] == "docling":
        markdown = convert_by_docling(input_path)
    else:
        # Guard: binary formats cannot be read as text
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
        markdown = convert_by_rules(text, lang=lang)  # ← pass lang

    # Step 3: Save output (with collision avoidance)
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(info["filename"])[0]
    output_path = os.path.join(output_dir, f"{base_name}.md")

    counter = 1
    while os.path.exists(output_path):
        output_path = os.path.join(output_dir, f"{base_name}_{counter}.md")
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
