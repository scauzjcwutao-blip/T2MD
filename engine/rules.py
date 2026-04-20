"""Rules engine — convert plain text to Markdown using pattern matching."""

import re


def convert_by_rules(text: str) -> str:
    """
    Convert plain text to Markdown using rule-based heuristics.

    Detects: headings, ordered lists, unordered lists, separators, paragraphs.
    """
    if not text or not text.strip():
        return ""

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

        # ── Heading guess: short line surrounded by blank lines ──
        if _is_likely_heading(lines, i):
            result.append(f"## {stripped}")
            i += 1
            continue

        # ── Ordered list: 1. or 1) or 1、 ──
        if re.match(r"^\d+[.、)]\s*", stripped):
            content = re.sub(r"^\d+[.、)]\s*", "", stripped)
            result.append(f"1. {content}")
            i += 1
            continue

        # ── Unordered list: - * · • ──
        if re.match(r"^[-*·•]\s+", stripped):
            content = re.sub(r"^[-*·•]\s+", "", stripped)
            result.append(f"- {content}")
            i += 1
            continue

        # ── Regular paragraph ──
        result.append(stripped)
        i += 1

    return _clean_output("\n".join(result))


def _is_likely_heading(lines: list, index: int) -> bool:
    """Check if the current line is likely a heading."""
    line = lines[index].strip()

    # Too long to be a heading
    if len(line) > 30:
        return False

    # Should not end with punctuation
    if line and line[-1] in ".,;!?)。，；！？）、":
        return False

    # Previous line is blank (or this is the first line)
    prev_empty = (index == 0) or (not lines[index - 1].strip())

    # Next line is blank (or this is the last line)
    next_empty = (index == len(lines) - 1) or (not lines[index + 1].strip())

    return prev_empty and next_empty


def _clean_output(text: str) -> str:
    """Clean up output: collapse multiple blank lines."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
