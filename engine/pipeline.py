"""Conversion pipeline — automatically selects Docling or rules engine."""

import os
from engine.classifier import classify
from engine.lang import detect
from engine.rules import convert_by_rules
from engine.docling_converter import convert_by_docling


def convert(input_path: str, output_dir: str = "output") -> str:
    """
    Main conversion function.

    Args:
        input_path: Path to the input file.
        output_dir: Directory for output files.

    Returns:
        Converted Markdown text.
    """
    # Step 1: Classify — decide which engine to use
    info = classify(input_path)
    print(f"[T2MD] File:   {info['filename']}")
    print(f"[T2MD] Format: {info['ext']}")
    print(f"[T2MD] Engine: {info['engine']}")

    # Step 2: Convert
    if info["engine"] == "docling":
        markdown = convert_by_docling(input_path)
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        lang = detect(text)
        print(f"[T2MD] Language: {lang}")
        markdown = convert_by_rules(text)

    # Step 3: Save output
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(info["filename"])[0]
    output_path = os.path.join(output_dir, f"{base_name}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"[T2MD] Output: {output_path}")
    return markdown


def convert_text(text: str) -> str:
    """
    Convert a text string directly (no file I/O).
    Used by GUI and tests.
    """
    return convert_by_rules(text)
