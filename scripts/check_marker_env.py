#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.metadata as metadata
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_PYTHON = (3, 11)
EXPECTED_PACKAGES = {
    "marker-pdf": "1.10.2",
    "surya-ocr": "0.17.1",
    "transformers": "4.57.6",
}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def version_of(package: str) -> str:
    return metadata.version(package)


def ensure_expected_runtime() -> None:
    if sys.version_info[:2] != EXPECTED_PYTHON:
        raise SystemExit(
            fail(
                f"Marker env must run on Python {EXPECTED_PYTHON[0]}.{EXPECTED_PYTHON[1]}; "
                f"got {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            )
        )



def ensure_expected_packages() -> None:
    mismatches: list[str] = []
    for package, expected in EXPECTED_PACKAGES.items():
        actual = version_of(package)
        print(f"{package}={actual}")
        if actual != expected:
            mismatches.append(f"{package}: expected {expected}, got {actual}")
    if mismatches:
        raise SystemExit(fail("; ".join(mismatches)))



def marker_single_path() -> Path:
    exe = Path(sys.executable).parent / "marker_single"
    if not exe.exists():
        raise SystemExit(fail(f"marker_single missing at {exe}"))
    return exe



def run_help(exe: Path) -> None:
    result = subprocess.run([str(exe), "--help"], capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise SystemExit(fail(f"marker_single --help failed rc={result.returncode}: {detail}"))
    print("marker_single_help=ok")



def run_smoke_extract(exe: Path, pdf_path: Path) -> None:
    if not pdf_path.exists():
        raise SystemExit(fail(f"Smoke PDF not found: {pdf_path}"))
    with tempfile.TemporaryDirectory(prefix="opteee-marker-smoke-") as tmpdir:
        out_dir = Path(tmpdir) / "out"
        out_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                str(exe),
                str(pdf_path),
                "--output_dir",
                str(out_dir),
                "--output_format",
                "markdown",
                "--disable_multiprocessing",
                "--disable_tqdm",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise SystemExit(fail(f"marker smoke extraction failed rc={result.returncode}: {detail}"))
        markdown_path = out_dir / pdf_path.stem / f"{pdf_path.stem}.md"
        if not markdown_path.exists():
            raise SystemExit(fail(f"marker smoke output missing: {markdown_path}"))
        text = markdown_path.read_text(encoding="utf-8").strip()
        if not text:
            raise SystemExit(fail("marker smoke output was empty"))
        print(f"marker_smoke_pdf={pdf_path}")
        print(f"marker_smoke_chars={len(text)}")



def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the dedicated OPTEEE Marker environment.")
    parser.add_argument(
        "--smoke-pdf",
        type=Path,
        help="Optional local PDF to extract as an end-to-end smoke test.",
    )
    args = parser.parse_args()

    ensure_expected_runtime()
    ensure_expected_packages()
    exe = marker_single_path()
    print(f"marker_single={exe}")
    run_help(exe)
    if args.smoke_pdf:
        run_smoke_extract(exe, args.smoke_pdf.resolve())
    print("status=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
