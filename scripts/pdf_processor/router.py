from __future__ import annotations

from pathlib import Path

from .backends import BackendUnavailableError, ExtractionBackendError, extract_with_baseline, extract_with_marker
from .models import ExtractionResult, OutputFormat
from .quality import inspect_pdf


def _candidate_order(*, route_hint: str, output_format: OutputFormat, allow_ocr: bool, prefer_speed: bool) -> list[str]:
    if route_hint == "marker_ocr":
        return ["marker", "baseline"] if allow_ocr else ["baseline"]
    if prefer_speed and output_format == "text":
        return ["baseline", "marker"]
    if output_format in {"markdown", "chunks"}:
        return ["marker", "baseline"]
    if route_hint == "marker":
        return ["marker", "baseline"]
    return ["baseline", "marker"]


def _acceptable(result: ExtractionResult) -> bool:
    if result.quality.empty:
        return False
    if result.quality.chars < 300:
        return False
    if result.quality.grade in {"excellent", "good"}:
        return True
    return result.quality.score >= 35


def extract_pdf(
    pdf_path: str | Path,
    *,
    backend: str = "auto",
    output_format: OutputFormat = "text",
    prefer_speed: bool = False,
    allow_ocr: bool = True,
    title: str | None = None,
    marker_command: str | None = None,
) -> ExtractionResult:
    path = Path(pdf_path)
    classification = inspect_pdf(path)

    if backend == "baseline":
        return extract_with_baseline(path, classification=classification, output_format=output_format, title=title)
    if backend == "marker":
        return extract_with_marker(
            path,
            classification=classification,
            output_format=output_format,
            allow_ocr=allow_ocr,
            title=title,
            marker_command=marker_command,
        )
    if backend != "auto":
        raise ValueError(f"unsupported backend: {backend}")

    attempts: list[str] = []
    failures: list[str] = []
    best_result: ExtractionResult | None = None
    best_score = -1.0
    order = _candidate_order(
        route_hint=classification.route_hint,
        output_format=output_format,
        allow_ocr=allow_ocr,
        prefer_speed=prefer_speed,
    )

    for candidate in order:
        attempts.append(candidate)
        try:
            if candidate == "baseline":
                result = extract_with_baseline(path, classification=classification, output_format=output_format, title=title)
            else:
                result = extract_with_marker(
                    path,
                    classification=classification,
                    output_format=output_format,
                    allow_ocr=allow_ocr,
                    title=title,
                    marker_command=marker_command,
                )
        except (BackendUnavailableError, ExtractionBackendError) as exc:
            failures.append(f"{candidate}:{exc}")
            continue

        result.backend_requested = "auto"
        result.route_reason = f"auto:{classification.route_hint}:attempted={','.join(attempts)}"
        if failures:
            result.warnings.extend(failures)
        if result.quality.score > best_score:
            best_result = result
            best_score = result.quality.score
        if _acceptable(result):
            return result

    if best_result is not None:
        best_result.warnings.extend(failures)
        best_result.route_reason = f"auto:{classification.route_hint}:best_of={','.join(attempts)}"
        return best_result

    raise ExtractionBackendError(
        f"all extraction backends failed for {path.name}: {'; '.join(failures) if failures else 'no attempts made'}"
    )
