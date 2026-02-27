"""
Utilities for conversation history shaping.
"""

from __future__ import annotations

import re


def sanitize_history_content(role: str, content: str) -> str:
    """
    Keep conversation context compact and text-only for RAG prompts.
    """
    if role != "assistant":
        return content

    cleaned = content
    cleaned = re.sub(
        r"<div class=\"video-references-section\">[\s\S]*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"(?m)^\s*#{1,6}\s*", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

