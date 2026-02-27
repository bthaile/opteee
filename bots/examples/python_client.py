"""
Minimal OPTEEE bot API client.

This helper is intentionally simple so any bot framework can wrap it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class OpteeeClient:
    base_url: str
    provider: str = "claude"
    num_results: int = 5
    timeout_seconds: int = 30

    def health(self) -> dict:
        response = requests.get(f"{self.base_url}/api/health", timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def create_conversation(self) -> str:
        response = requests.post(
            f"{self.base_url}/api/conversations",
            json={},
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()["id"]

    def chat(self, query: str, conversation_id: Optional[str] = None) -> dict:
        payload = {
            "query": query,
            "provider": self.provider,
            "num_results": self.num_results,
            "format": "json",
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    client = OpteeeClient(base_url="http://localhost:7860")
    print("Health:", client.health())

    conv_id = client.create_conversation()
    print("Conversation ID:", conv_id)

    first = client.chat("What is gamma in options trading?", conversation_id=conv_id)
    print("Answer 1:", first["answer"][:300], "...")

    second = client.chat("How does that affect risk?", conversation_id=conv_id)
    print("Answer 2:", second["answer"][:300], "...")
