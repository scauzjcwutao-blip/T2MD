"""T2MD engine — Docling + Rules-based dual-mode converter."""

# 轻量暴露最常用的接口，方便外部调用
from .convert import convert, convert_text
from .lang import detect

__all__ = ["convert", "convert_text", "detect"]
