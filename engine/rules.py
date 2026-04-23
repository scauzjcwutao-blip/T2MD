"""Rules engine — convert plain text to Markdown using pattern matching."""

import re


def convert_by_rules(text: str, lang: str = "en") -> str:
    """
    Convert plain text to Markdown using rule-based heuristics.

    Now supports language-aware rules (especially Chinese/Japanese).
    """
    if not text or not text.strip():
        return ""

    # Normalize language code
    lang = lang.lower()[:2] if lang else "en"

    lines = text.strip().split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # ── Empty line ──
        if not stripped:
            result.append("")
            i += 1
            continue

        # ── Separator (---, ===, ***) ──
        if re.match(r"^[-=*]{3,}\s*$", stripped):
            result.append("---")
            i += 1
            continue

        # ── Existing Markdown heading ──
        if re.match(r"^#{1,6}\s+", stripped):
            result.append(stripped)
            i += 1
            continue

        # ── Setext-style heading: line followed by === or --- ──
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if re.match(r"^={3,}\s*$", next_line):
                result.append(f"# {stripped}")
                i += 2
                continue
            if re.match(r"^-{3,}\s*$", next_line):
                result.append(f"## {stripped}")
                i += 2
                continue

        # ── Heading guess (language-aware) ──
        if _is_likely_heading(lines, i, lang):
            result.append(f"## {stripped}")
            i += 1
            continue

        # ── Ordered list: 1. 1) 1、 （支持中文常见序号）──
        m = re.match(r"^(\d+|[一二三四五六七八九十]+)[.、)]\s*(.*)$", stripped)
        if m:
            num, content = m.group(1), m.group(2)
            result.append(f"{num}. {content}")
            i += 1
            continue

        # ── Unordered list（增加更多中文常见项目符号）──
        if re.match(r"^[-*·•○◆◇■□]\s+", stripped):
            content = re.sub(r"^[-*·•○◆◇■□]\s+", "", stripped)
            result.append(f"- {content}")
            i += 1
            continue

        # ── Regular paragraph ──
        result.append(stripped)
        i += 1

    return _clean_output("\n".join(result))


# Language-aware punctuation that signals "this is a sentence, not a heading"
_SENTENCE_ENDING = {
    "en": set(".,;:!?)\"'"),
    "zh": set("。，；：！？）」》…、"),
    "ja": set("。、，；：！？）」】…"),
    "ko": set(".,;:!?)\"'。、，；：！？)"),
}

def _is_likely_heading(lines: list, index: int, lang: str = "en") -> bool:
    """Check if the current line is likely a heading (now language-aware)."""
    line = lines[index].strip()

    # Language-specific max length (中文标题常较长)
    max_len = 50 if lang in ("zh", "ja", "ko") else 30
    if len(line) > max_len:
        return False

    # Must contain at least one letter/CJK character
    if not re.search(r"[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]", line):
        return False

    # Should not end with sentence-ending punctuation (语言感知)
    ending_punct = _SENTENCE_ENDING.get(lang, _SENTENCE_ENDING["en"])
    if line and line[-1] in ending_punct:
        return False

    # Should not look like a list item
    if re.match(r"^(\d+|[一二三四五六七八九十]+)[.、)]|[-*·•○◆◇■□]\s", line):
        return False

    # Previous and next line should be blank (or edge of document)
    prev_empty = (index == 0) or (not lines[index - 1].strip())
    next_empty = (index == len(lines) - 1) or (not lines[index + 1].strip())

    return prev_empty and next_empty


def _clean_output(text: str) -> str:
    """Clean up output: collapse multiple blank lines."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
