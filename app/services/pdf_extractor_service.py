from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path


class PDFExtractorService:
    def __init__(self, repo_root: Path | None = None) -> None:
        self.repo_root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
        self.pipeline_python = self.repo_root / "venv" / "bin" / "python"
        self.processor_script = self.repo_root / "process_pdfs.py"

    def extract(self, pdf_path: str, *, backend: str = "auto", allow_ocr: bool = True, marker_command: str | None = None) -> dict:
        target = Path(pdf_path)
        if not target.is_absolute():
            target = (self.repo_root / target).resolve()
        if not target.exists():
            raise FileNotFoundError(f"PDF not found: {target}")
        if target.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF: {target}")
        if not self.pipeline_python.exists():
            raise FileNotFoundError(f"Pipeline venv missing: {self.pipeline_python}")
        if not self.processor_script.exists():
            raise FileNotFoundError(f"Processor script missing: {self.processor_script}")

        with tempfile.TemporaryDirectory(prefix="opteee-pdf-extract-") as tmpdir:
            out_json = Path(tmpdir) / "result.json"
            cmd = [
                str(self.pipeline_python),
                str(self.processor_script),
                "--pdf",
                str(target),
                "--source",
                str(target.parent),
                "--extract-json",
                str(out_json),
                "--pdf-backend",
                backend,
            ]
            if not allow_ocr:
                cmd.append("--no-ocr")
            if marker_command:
                cmd.extend(["--marker-command", marker_command])

            env = os.environ.copy()
            env.setdefault("PYTHONUNBUFFERED", "1")
            result = subprocess.run(cmd, cwd=self.repo_root, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                detail = (result.stderr or result.stdout).strip()
                raise RuntimeError(f"PDF extraction failed rc={result.returncode}: {detail}")
            if not out_json.exists():
                raise RuntimeError("PDF extraction completed without output JSON")
            payload = json.loads(out_json.read_text(encoding="utf-8"))
            payload.setdefault("service_logs", {})
            payload["service_logs"]["stdout"] = result.stdout.strip()
            payload["service_logs"]["stderr"] = result.stderr.strip()
            return payload
