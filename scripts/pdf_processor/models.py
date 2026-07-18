from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

BackendName = Literal["baseline", "marker", "auto"]
OutputFormat = Literal["text", "markdown", "chunks"]


@dataclass(slots=True)
class DocumentClassification:
    pdf_path: Path
    page_count: int = 0
    sampled_pages: int = 0
    sampled_text_chars: int = 0
    chars_per_sampled_page: float = 0.0
    likely_born_digital: bool = False
    likely_scanned: bool = False
    route_hint: str = "unknown"
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class QualityReport:
    chars: int = 0
    lines: int = 0
    chars_per_page: float = 0.0
    empty: bool = False
    has_abstract: bool = False
    title_present: bool = False
    section_markers: int = 0
    equation_markers: int = 0
    table_pipes: int = 0
    weird_char_count: int = 0
    score: float = 0.0
    grade: str = "poor"
    flags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Chunk:
    text: str
    page: int | None = None
    block_type: str = "paragraph"
    section_hierarchy: list[str] = field(default_factory=list)
    source_backend: str = ""
    quality_flags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ExtractionResult:
    pdf_path: Path
    backend_requested: BackendName
    backend_used: str
    output_format: OutputFormat
    route_reason: str
    classification: DocumentClassification
    quality: QualityReport
    runtime_sec: float
    text: str = ""
    markdown: str = ""
    chunks: list[Chunk] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def primary_text(self) -> str:
        return self.markdown or self.text

    def to_dict(self) -> dict:
        return {
            "pdf_path": str(self.pdf_path),
            "backend_requested": self.backend_requested,
            "backend_used": self.backend_used,
            "output_format": self.output_format,
            "route_reason": self.route_reason,
            "classification": {
                "page_count": self.classification.page_count,
                "sampled_pages": self.classification.sampled_pages,
                "sampled_text_chars": self.classification.sampled_text_chars,
                "chars_per_sampled_page": self.classification.chars_per_sampled_page,
                "likely_born_digital": self.classification.likely_born_digital,
                "likely_scanned": self.classification.likely_scanned,
                "route_hint": self.classification.route_hint,
                "notes": list(self.classification.notes),
            },
            "quality": {
                "chars": self.quality.chars,
                "lines": self.quality.lines,
                "chars_per_page": self.quality.chars_per_page,
                "empty": self.quality.empty,
                "has_abstract": self.quality.has_abstract,
                "title_present": self.quality.title_present,
                "section_markers": self.quality.section_markers,
                "equation_markers": self.quality.equation_markers,
                "table_pipes": self.quality.table_pipes,
                "weird_char_count": self.quality.weird_char_count,
                "score": self.quality.score,
                "grade": self.quality.grade,
                "flags": list(self.quality.flags),
            },
            "runtime_sec": self.runtime_sec,
            "text": self.text,
            "markdown": self.markdown,
            "chunks": [
                {
                    "text": c.text,
                    "page": c.page,
                    "block_type": c.block_type,
                    "section_hierarchy": list(c.section_hierarchy),
                    "source_backend": c.source_backend,
                    "quality_flags": list(c.quality_flags),
                }
                for c in self.chunks
            ],
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }
