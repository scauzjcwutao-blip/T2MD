"""T2MD engine — Docling + Rules-based dual-mode converter."""

# 当前主转换文件是 pipeline.py
from .pipeline import convert, convert_text, convert_batch   # ← 必须加上这一项
from .lang import detect

__all__ = ["convert", "convert_text", "convert_batch", "detect"]
