"""
Minimal OPTEEE bot API client.

This helper is intentionally simple so any bot framework can wrap it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import requests


@dataclass
class OpteeeClient:
    """Minimal OPTEEE API client with chat + wiki helpers.

    The wiki methods mirror the REST endpoints documented in README.md and
    bots/README.md so downstream Telegram/Slack/webhook integrations can drill
    from chat results into the synthesized knowledge layer.
    """

    base_url: str
    provider: str = "claude"
    num_results: int = 5
    timeout_seconds: int = 30

    def _get(self, path: str, **params: Any) -> dict:
        response = requests.get(
            f"{self.base_url}{path}",
            params={k: v for k, v in params.items() if v is not None},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, payload: dict) -> dict:
        response = requests.post(
            f"{self.base_url}{path}",
            json=payload,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def health(self) -> dict:
        return self._get("/api/health")

    def create_conversation(self) -> str:
        return self._post("/api/conversations", {})["id"]

    def chat(self, query: str, conversation_id: Optional[str] = None) -> dict:
        payload = {
            "query": query,
            "provider": self.provider,
            "num_results": self.num_results,
            "format": "json",
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id

        return self._post("/api/chat", payload)

    def wiki_index_document(self, include_html: bool = False) -> dict:
        return self._get("/api/wiki/index/document", include_html=include_html)

    def wiki_index(self) -> dict:
        return self._get("/api/wiki/index")

    def wiki_graph(self) -> dict:
        return self._get("/api/wiki/graph.json")

    def wiki_page(self, path: str, output_format: str = "json") -> dict:
        return self._get(f"/api/wiki/pages/{path}", format=output_format)

    def expand_chat_with_wiki(self, chat_response: dict) -> list[dict]:
        """Fetch full wiki pages for the chat response's top-level wiki references."""
        pages = []
        for ref in chat_response.get("wiki_references", []):
            page_path = ref.get("path")
            if not page_path:
                continue
            page = self.wiki_page(page_path, output_format="json")
            pages.append({"reference": ref, "page": page})
        return pages


if __name__ == "__main__":
    client = OpteeeClient(base_url="http://localhost:7860")
    print("Health:", client.health())

    conv_id = client.create_conversation()
    print("Conversation ID:", conv_id)

    first = client.chat("What is gamma in options trading?", conversation_id=conv_id)
    print("Answer 1:", first["answer"][:300], "...")
    print("Wiki refs:", [ref.get("path") for ref in first.get("wiki_references", [])])

    for expanded in client.expand_chat_with_wiki(first)[:2]:
        page = expanded["page"]
        print(
            "Wiki page:",
            expanded["reference"].get("path"),
            "title=",
            page.get("frontmatter", {}).get("title"),
        )

    second = client.chat("How does that affect risk?", conversation_id=conv_id)
    print("Answer 2:", second["answer"][:300], "...")
