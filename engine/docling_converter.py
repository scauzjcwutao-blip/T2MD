"""Docling engine — convert PDF/Word/HTML/images to Markdown with pdfplumber fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

# 核心依赖（fallback 需要）
from engine.lang import detect
from engine.rules import convert_by_rules


class DoclingConversionError(Exception):
    """Raised when Docling fails to convert a document."""


# Module-level singleton — initialized lazily
_converter: Optional["DocumentConverter"] = None


def _get_converter():
    """Return a shared DocumentConverter instance (lazy init)."""
    global _converter
    if _converter is None:
        try:
            from docling.document_converter import DocumentConverter
            _converter = DocumentConverter()
        except ImportError as exc:
            raise ImportError(
                "Docling is not installed. Install with: pip install docling"
            ) from exc
    return _converter


def _pdf_fallback(file_path: str) -> str:
    """Extract text from PDF via pdfplumber when docling is unavailable."""
    try:
        import pdfplumber
    except ImportError as exc:
        raise ImportError(
            "Neither docling nor pdfplumber is installed. "
            "Install pdfplumber with: pip install pdfplumber"
        ) from exc

    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages.append(text)

    raw = "\n\n".join(pages)

    if not raw.strip():
        return ""

    # 语言检测（和 convert.py 主流程完全一致）
    lang = detect(raw)
    print(f"[T2MD] Language: {lang} (PDF fallback)")

    return convert_by_rules(raw, lang=lang)


def convert_by_docling(file_path: str) -> str:
    """
    Convert a document to Markdown using Docling.
    Automatically falls back to pdfplumber if Docling is unavailable or fails.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        converter = _get_converter()
        result = converter.convert(file_path)
        markdown = result.document.export_to_markdown()

        if not markdown or not markdown.strip():
            raise DoclingConversionError(
                f"Docling returned empty output for: {file_path}"
            )

        print("[T2MD] Engine: docling (success)")
        return markdown

    except Exception as e:   # 包含 docling 未安装、转换失败等所有情况
        print(f"[T2MD] Docling failed: {e}, falling back to pdfplumber...")
        return _pdf_fallback(file_path)
