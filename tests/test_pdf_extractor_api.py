import importlib
import os
from pathlib import Path

from fastapi.testclient import TestClient


def test_pdf_extract_endpoint_returns_payload(monkeypatch):
    os.environ["TEST_MODE"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///./test_pdf_extract_api.db"
    import main

    main_module = importlib.reload(main)

    def fake_extract(pdf_path, *, backend="auto", allow_ocr=True, marker_command=None):
        return {
            "pdf_path": pdf_path,
            "backend_used": backend,
            "route_reason": "auto:marker:attempted=marker",
            "quality": {"grade": "good", "score": 77.5},
            "markdown": "# Sample\n\nhello",
        }

    monkeypatch.setattr(main_module.pdf_extractor_service, "extract", fake_extract)
    client = TestClient(main_module.app)

    response = client.post(
        "/api/pdf/extract",
        json={"pdf_path": "docs/sample.pdf", "backend": "auto", "allow_ocr": True},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["payload"]["backend_used"] == "auto"
    assert body["payload"]["quality"]["grade"] == "good"


def test_process_pdfs_extract_pdf_text_uses_router(monkeypatch, tmp_path):
    import process_pdfs

    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(b"%PDF-1.4\n%stub")

    class DummyResult:
        primary_text = "Abstract\n\nThis is a test document."

        def to_dict(self):
            return {
                "backend_used": "marker",
                "route_reason": "auto:marker:attempted=marker",
                "quality": {"grade": "good", "score": 65.0},
                "markdown": self.primary_text,
                "text": self.primary_text,
            }

    def fake_extract_pdf(pdf_path, **kwargs):
        assert Path(pdf_path) == pdf
        assert kwargs["backend"] == "auto"
        return DummyResult()

    monkeypatch.setattr(process_pdfs, "extract_pdf", fake_extract_pdf)
    payload = process_pdfs.extract_pdf_text(str(pdf), backend="auto")
    assert payload["backend_used"] == "marker"
    assert payload["quality"]["grade"] == "good"
