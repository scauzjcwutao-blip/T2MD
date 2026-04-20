"""Docling engine — convert PDF/Word/HTML/images to Markdown."""

from __future__ import annotations  # ← 放在文件最顶部，支持 3.9

from pathlib import Path
from typing import Optional

from docling.document_converter import DocumentConverter


class DoclingConversionError(Exception):
    """Raised when Docling fails to convert a document."""


# Module-level singleton — initialized lazily
_converter: Optional[DocumentConverter] = None


def _get_converter() -> DocumentConverter:
    """Return a shared DocumentConverter instance (lazy init)."""
    global _converter
    if _converter is None:
        _converter = DocumentConverter()
    return _converter


def convert_by_docling(file_path: str) -> str:
    """
    Convert a document to Markdown using Docling.

    Supports: PDF, DOCX, PPTX, HTML, images.

    Args:
        file_path: Path to the input file.

    Returns:
        Markdown string.

    Raises:
        FileNotFoundError: If the file does not exist.
        DoclingConversionError: If Docling fails.
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

        return markdown

    except DoclingConversionError:
        raise
    except Exception as e:
        raise DoclingConversionError(
            f"Docling conversion failed for {file_path}: {e}"
        ) from e
