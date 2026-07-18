from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from .models import DocumentClassification, QualityReport


def inspect_pdf(pdf_path: str | Path, sample_pages: int = 3) -> DocumentClassification:
    path = Path(pdf_path)
    notes: list[str] = []
    sampled_text_chars = 0
    sampled_pages_actual = 0

    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    for page in reader.pages[:sample_pages]:
        sampled_pages_actual += 1
        try:
            sampled_text_chars += len(page.extract_text() or "")
        except Exception as exc:  # pragma: no cover
            notes.append(f"page_extract_error:{type(exc).__name__}")

    chars_per_sampled_page = sampled_text_chars / max(sampled_pages_actual, 1)
    likely_scanned = sampled_text_chars < 100
    likely_born_digital = sampled_text_chars > 500

    if likely_scanned:
        route_hint = "marker_ocr"
        notes.append("very_low_text_layer_detected")
    elif likely_born_digital:
        route_hint = "marker"
        notes.append("strong_text_layer_detected")
    else:
        route_hint = "baseline"
        notes.append("mixed_text_layer_detected")

    return DocumentClassification(
        pdf_path=path,
        page_count=page_count,
        sampled_pages=sampled_pages_actual,
        sampled_text_chars=sampled_text_chars,
        chars_per_sampled_page=chars_per_sampled_page,
        likely_born_digital=likely_born_digital,
        likely_scanned=likely_scanned,
        route_hint=route_hint,
        notes=notes,
    )


_WEIRD_CHAR_RE = re.compile(r"[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffd\u00a1\u00a2]")
_SECTION_RE = re.compile(r"(?m)^(#{1,6}\s|\d+(?:\.\d+)*[.)]?\s+[A-Z])")
_EQUATION_RE = re.compile(r"(?m)(\$.*?\$|\\\(|\\\)|\\begin\{|\bequation\b|=\s*[A-Za-z0-9(])")


def assess_quality(text: str, *, page_count: int = 0, title: str | None = None) -> QualityReport:
    normalized = text or ""
    stripped = normalized.strip()
    chars = len(normalized)
    lines = len(normalized.splitlines()) if normalized else 0
    chars_per_page = chars / max(page_count, 1)
    weird_char_count = len(_WEIRD_CHAR_RE.findall(normalized))
    section_markers = len(_SECTION_RE.findall(normalized))
    equation_markers = len(_EQUATION_RE.findall(normalized))
    table_pipes = normalized.count("|")
    lowered = normalized.lower()
    has_abstract = "abstract" in lowered
    title_present = bool(title and title.lower() in lowered[:2000])
    empty = not stripped

    score = 0.0
    flags: list[str] = []
    if empty:
        flags.append("empty_text")
    if chars < 500:
        flags.append("low_text_volume")
    if page_count and chars_per_page < 150:
        flags.append("low_chars_per_page")
    if weird_char_count > 20:
        flags.append("encoding_noise")
    if table_pipes == 0:
        flags.append("no_table_markers")
    if equation_markers == 0:
        flags.append("no_equation_markers")

    score += min(chars / 8000.0, 1.0) * 40.0
    score += min(chars_per_page / 1500.0, 1.0) * 20.0
    score += min(section_markers / 12.0, 1.0) * 15.0
    score += min(equation_markers / 10.0, 1.0) * 10.0
    score += min(table_pipes / 40.0, 1.0) * 10.0
    if has_abstract:
        score += 3.0
    if title_present:
        score += 2.0
    score -= min(weird_char_count, 40) * 0.5
    score = max(score, 0.0)

    if score >= 75:
        grade = "excellent"
    elif score >= 55:
        grade = "good"
    elif score >= 35:
        grade = "fair"
    else:
        grade = "poor"

    return QualityReport(
        chars=chars,
        lines=lines,
        chars_per_page=chars_per_page,
        empty=empty,
        has_abstract=has_abstract,
        title_present=title_present,
        section_markers=section_markers,
        equation_markers=equation_markers,
        table_pipes=table_pipes,
        weird_char_count=weird_char_count,
        score=round(score, 2),
        grade=grade,
        flags=flags,
    )
