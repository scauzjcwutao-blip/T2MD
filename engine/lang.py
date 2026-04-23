"""Language detection and trilingual UI strings (English / Chinese / German / Japanese / Korean)."""

from langdetect import detect as _detect
from langdetect import LangDetectException


# ──────────────────────────────────────────────
# Part 1: Language detection
# ──────────────────────────────────────────────

# Map langdetect codes to our internal codes
_LANG_MAP = {
    "zh-cn": "zh",
    "zh-tw": "zh",
    "ja": "ja",      # ← 新增
    "ko": "ko",      # ← 新增
    "en": "en",
    "de": "de",
}


def detect(text: str) -> str:
    """
    Detect the language of the given text.

    Returns:
        Normalized language code: 'zh', 'en', 'de', 'ja', 'ko'...
        Returns 'unknown' on failure or empty text.
    """
    if not text or not text.strip():
        return "unknown"

    try:
        raw = _detect(text)
        return _LANG_MAP.get(raw, raw)  # 未知语言直接返回原码（如 'fr'）
    except (LangDetectException, Exception):  # 捕获所有可能异常，更稳健
        return "unknown"


# ──────────────────────────────────────────────
# Part 2: Trilingual UI strings
# ──────────────────────────────────────────────

TEXTS = {
    "en": {
        "author": "Author",
        "date": "Date",
        "category": "Category",
        "source": "Source",
        "processing": "Processing",
        "done": "Done",
        "error": "Error",
        "skipped": "Skipped",
        "watching": "Watching directory",
        "no_files": "No supported files found",
        "converted": "Converted",
        "files_processed": "files processed",
        "output_dir": "Output directory",
        "select_src": "Select Source",
        "select_dst": "Select Destination",
        "start": "Start Conversion",
        "language": "Language",
        "recursive": "Include subdirectories",
        "status": "Status",
        "ready": "Ready",
        "converting": "Converting…",
        "complete": "Conversion complete",
        "src_not_found": "Source path does not exist",
        "dst_create_fail": "Cannot create output directory",
    },
    "zh": {
        "author": "作者",
        "date": "日期",
        "category": "分类",
        "source": "来源",
        "processing": "处理中",
        "done": "完成",
        "error": "错误",
        "skipped": "已跳过",
        "watching": "正在监视目录",
        "no_files": "未找到支持的文件",
        "converted": "已转换",
        "files_processed": "个文件已处理",
        "output_dir": "输出目录",
        "select_src": "选择来源",
        "select_dst": "选择目标",
        "start": "开始转换",
        "language": "语言",
        "recursive": "包含子目录",
        "status": "状态",
        "ready": "就绪",
        "converting": "转换中…",
        "complete": "转换完成",
        "src_not_found": "来源路径不存在",
        "dst_create_fail": "无法创建输出目录",
    },
    "de": {  # ...（保持不变）
        "author": "Autor",
        "date": "Datum",
        "category": "Kategorie",
        "source": "Quelle",
        "processing": "Verarbeitung",
        "done": "Fertig",
        "error": "Fehler",
        "skipped": "Übersprungen",
        "watching": "Verzeichnis wird überwacht",
        "no_files": "Keine unterstützten Dateien gefunden",
        "converted": "Konvertiert",
        "files_processed": "Dateien verarbeitet",
        "output_dir": "Ausgabeverzeichnis",
        "select_src": "Quelle wählen",
        "select_dst": "Ziel wählen",
        "start": "Konvertierung starten",
        "language": "Sprache",
        "recursive": "Unterverzeichnisse einbeziehen",
        "status": "Status",
        "ready": "Bereit",
        "converting": "Konvertiere…",
        "complete": "Konvertierung abgeschlossen",
        "src_not_found": "Quellpfad existiert nicht",
        "dst_create_fail": "Ausgabeverzeichnis kann nicht erstellt werden",
    },
}

# All supported UI languages
SUPPORTED_LANGUAGES = list(TEXTS.keys())


def get_text(key: str, lang: str = "en") -> str:
    """Return a UI string for *key* in the given language."""
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)
