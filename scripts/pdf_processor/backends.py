from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from .models import Chunk, DocumentClassification, ExtractionResult, OutputFormat
from .quality import assess_quality


class ExtractionBackendError(RuntimeError):
    pass


class BackendUnavailableError(ExtractionBackendError):
    pass


def _run_pdftotext(path: Path) -> str:
    exe = shutil.which("pdftotext")
    if not exe:
        return ""
    result = subprocess.run([exe, str(path), "-"], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout
    return ""


def _run_pypdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def extract_with_baseline(
    pdf_path: str | Path,
    *,
    classification: DocumentClassification,
    output_format: OutputFormat = "text",
    title: str | None = None,
) -> ExtractionResult:
    path = Path(pdf_path)
    started = time.monotonic()
    text = _run_pdftotext(path)
    warnings: list[str] = []
    metadata = {"baseline_method": "pdftotext" if text else "pypdf"}
    if not text:
        text = _run_pypdf(path)
        warnings.append("pdftotext_unavailable_or_empty")
    quality = assess_quality(text, page_count=classification.page_count, title=title)
    runtime_sec = round(time.monotonic() - started, 2)
    markdown = text if output_format == "markdown" else ""
    chunks = []
    if output_format == "chunks" and text.strip():
        chunks = [Chunk(text=text, page=None, block_type="document", source_backend="baseline", quality_flags=list(quality.flags))]
    return ExtractionResult(
        pdf_path=path,
        backend_requested="baseline",
        backend_used="baseline",
        output_format=output_format,
        route_reason="baseline_direct_request",
        classification=classification,
        quality=quality,
        runtime_sec=runtime_sec,
        text=text,
        markdown=markdown,
        chunks=chunks,
        warnings=warnings,
        metadata=metadata,
    )


def _marker_command(explicit: str | None = None) -> str:
    repo_root = Path(__file__).resolve().parents[2]
    candidates = [
        explicit,
        os.environ.get("MARKER_SINGLE_COMMAND"),
        str(repo_root / ".venv-marker" / "bin" / "marker_single"),
        str(repo_root / "scripts" / "marker_single_compat.py"),
        str(Path(sys.executable).parent / "marker_single"),
        str(repo_root / "venv" / "bin" / "marker_single"),
        shutil.which("marker_single"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
        resolved = shutil.which(candidate)
        if resolved:
            return str(resolved)
    raise BackendUnavailableError(
        "marker_single command not available; set MARKER_SINGLE_COMMAND or bootstrap the dedicated .venv-marker environment"
    )


def extract_with_marker(
    pdf_path: str | Path,
    *,
    classification: DocumentClassification,
    output_format: OutputFormat = "markdown",
    allow_ocr: bool = True,
    title: str | None = None,
    marker_command: str | None = None,
) -> ExtractionResult:
    path = Path(pdf_path)
    started = time.monotonic()
    cmd = _marker_command(marker_command)
    warnings: list[str] = []
    requested_format = output_format
    marker_format = "chunks" if output_format == "chunks" else "markdown"

    with tempfile.TemporaryDirectory(prefix="opteee-marker-") as tmpdir:
        out_dir = Path(tmpdir) / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        argv = [
            cmd,
            str(path),
            "--output_dir",
            str(out_dir),
            "--output_format",
            marker_format,
            "--disable_multiprocessing",
            "--disable_tqdm",
        ]
        if not allow_ocr:
            argv.append("--disable_ocr")
        result = subprocess.run(argv, capture_output=True, text=True)
        runtime_sec = round(time.monotonic() - started, 2)
        if result.returncode != 0:
            raise ExtractionBackendError(
                f"marker extraction failed rc={result.returncode}: {(result.stderr or result.stdout).strip()}"
            )

        doc_dir = out_dir / path.stem
        if not doc_dir.exists():
            raise ExtractionBackendError(f"marker output directory missing: {doc_dir}")

        markdown = ""
        text = ""
        chunks: list[Chunk] = []
        metadata = {
            "marker_stdout": result.stdout.strip(),
            "marker_stderr": result.stderr.strip(),
            "marker_output_format": marker_format,
        }

        if marker_format == "markdown":
            md_path = doc_dir / f"{path.stem}.md"
            if not md_path.exists():
                raise ExtractionBackendError(f"marker markdown output missing: {md_path}")
            markdown = md_path.read_text()
            text = markdown
        else:
            json_path = doc_dir / f"{path.stem}.json"
            if not json_path.exists():
                raise ExtractionBackendError(f"marker chunks output missing: {json_path}")
            payload = json.loads(json_path.read_text())
            rendered: list[str] = []
            for block in payload.get("children", []):
                block_text = (block.get("text") or "").strip()
                if block_text:
                    rendered.append(block_text)
                    chunks.append(
                        Chunk(
                            text=block_text,
                            page=block.get("page_id"),
                            block_type=block.get("block_type", "block"),
                            source_backend="marker",
                            quality_flags=[],
                        )
                    )
            text = "\n\n".join(rendered)

        quality = assess_quality(text or markdown, page_count=classification.page_count, title=title)
        if classification.likely_scanned and quality.chars < 300:
            warnings.append("marker_ocr_sparse_output")
        return ExtractionResult(
            pdf_path=path,
            backend_requested="marker",
            backend_used="marker",
            output_format=requested_format,
            route_reason="marker_direct_request",
            classification=classification,
            quality=quality,
            runtime_sec=runtime_sec,
            text=text,
            markdown=markdown,
            chunks=chunks,
            warnings=warnings,
            metadata=metadata,
        )
