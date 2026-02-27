import importlib
import json
import os
import unittest

from pydantic import ValidationError
from fastapi.testclient import TestClient

from app.models.chat_models import ChatRequest
from app.services.formatters import ResponseFormatter


class BotApiContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TEST_MODE"] = "true"
        os.environ["DATABASE_URL"] = "sqlite:///./test_bot_api.db"
        import main

        cls.main_module = importlib.reload(main)
        cls.client = TestClient(cls.main_module.app)

    def test_chat_request_rejects_legacy_discord_format(self):
        with self.assertRaises(ValidationError):
            ChatRequest(query="test", format="discord")

    def test_json_formatter_returns_plain_text_and_structured_sources(self):
        formatter = ResponseFormatter()
        result = formatter.format_response(
            answer="### Header **Bold** <b>HTML</b>",
            sources=[
                {
                    "source_type": "video",
                    "title": "Sample Video",
                    "content": "<p>Some transcript excerpt</p>",
                    "url": "https://example.com",
                    "video_url_with_timestamp": "https://example.com&t=30",
                    "start_timestamp_seconds": 30,
                }
            ],
            format_type="json",
        )

        payload = result["formatted_content"]
        self.assertEqual(result["format"], "json")
        self.assertNotIn("<", payload["answer"])
        self.assertNotIn("**", payload["answer"])
        self.assertIsInstance(payload["raw_sources"], list)

        sources_json = json.loads(payload["sources"])
        self.assertIsInstance(sources_json, list)
        self.assertEqual(sources_json[0]["title"], "Sample Video")

    def test_chat_endpoint_json_returns_conversation_id(self):
        response = self.client.post(
            "/api/chat",
            json={
                "query": "What is gamma?",
                "provider": "claude",
                "num_results": 3,
                "format": "json",
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("conversation_id", body)
        self.assertTrue(body["conversation_id"])
        self.assertIsInstance(body.get("raw_sources"), list)

