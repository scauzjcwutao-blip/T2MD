"""T2MD engine — Docling + Rules-based dual-mode converter."""

# 轻量暴露核心接口（当前主文件是 pipeline.py）
from .pipeline import convert, convert_text
from .lang import detect

__all__ = ["convert", "convert_text", "detect"]
