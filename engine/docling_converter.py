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


def _table_to_markdown(table: list) -> str:
    """将 pdfplumber 提取的表格转为 Markdown 表格（专为 10-K、年报等设计）"""
    if not table or not table[0]:
        return ""
    # 表头
    header = "| " + " | ".join(str(cell) if cell is not None else "" for cell in table[0]) + " |"
    separator = "| " + " | ".join("---" for _ in table[0]) + " |"
    # 数据行
    rows = [
        "| " + " | ".join(str(cell) if cell is not None else "" for cell in row) + " |"
        for row in table[1:]
    ]
    return "\n".join([header, separator] + rows)


def _pdf_fallback(file_path: str) -> str:
    """Extract text from PDF via pdfplumber when docling is unavailable.
    已优化：支持表格提取（适合10-K、年报等结构化文件）
    """
    try:
        import pdfplumber
    except ImportError as exc:
        raise ImportError(
            "Neither docling nor pdfplumber is installed. "
            "Install pdfplumber with: pip install pdfplumber"
        ) from exc

    pages = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # 1. 提取普通文本（优化布局）
                text = page.extract_text(
                    layout=True,
                    x_tolerance=3,
                    y_tolerance=3
                ) or ""

                # 2. 提取表格（关键改进）
                tables = page.extract_tables()
                if tables:
                    text += f"\n\n### Page {page_num} Tables\n\n"
                    for i, table in enumerate(tables, 1):
                        if table:
                            markdown_table = _table_to_markdown(table)
                            text += f"**Table {i}**\n{markdown_table}\n\n"

                # 3. 图表提示（10-K 常用）
                if page.images:
                    text += f"**Figures on page {page_num}**: {len(page.images)} image(s) detected.\n"

                if text.strip():
                    pages.append(text)

    except Exception as e:   # 捕获损坏、加密、无法解析等所有异常
        print(f"[T2MD] ⚠️ PDF may be corrupted, encrypted or unreadable: {e}")
        print(f"[T2MD] File: {file_path}")
        return f"# ⚠️ PDF 转换失败\n\n文件可能已损坏、加密或无法解析：\n{file_path}\n\n错误信息：{e}\n"

    raw = "\n\n".join(pages)

    if not raw.strip():
        print(f"[T2MD] ⚠️ PDF extracted empty content: {file_path}")
        return ""

    # 语言检测（和 pipeline.py 主流程完全一致）
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
