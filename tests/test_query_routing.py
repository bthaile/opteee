import importlib
import os
import unittest
from unittest.mock import patch

from app.models.chat_models import ChatRequest
import rag_pipeline


class QueryRoutingTests(unittest.TestCase):
    def test_chat_request_defaults_effort_to_low(self):
        request = ChatRequest(query="What is gamma?")

        self.assertEqual(request.effort, "low")
        self.assertIsNone(request.model)

    def test_chat_request_accepts_model_and_effort(self):
        request = ChatRequest(
            query="Compare rolling approaches",
            provider="claude",
            effort="medium",
            model="claude-sonnet-4-5",
        )

        self.assertEqual(request.effort, "medium")
        self.assertEqual(request.model, "claude-sonnet-4-5")

    def test_resolve_llm_selection_uses_explicit_model_override(self):
        with patch.dict(
            os.environ,
            {
                "LLM_PROVIDER": "claude",
                "DEFAULT_MODEL_LOW": "claude-haiku-4-5",
                "DEFAULT_MODEL_MEDIUM": "claude-sonnet-4-5",
                "CLAUDE_MODEL_LOW": "claude-haiku-4-5",
                "CLAUDE_MODEL_MEDIUM": "claude-sonnet-4-5",
            },
            clear=False,
        ):
            importlib.reload(rag_pipeline)
            selection = rag_pipeline.resolve_llm_selection(
                provider="claude",
                model="claude-3-7-sonnet-latest",
                effort="medium",
            )

        self.assertEqual(selection["provider"], "claude")
        self.assertEqual(selection["model"], "claude-3-7-sonnet-latest")
        self.assertEqual(selection["effort"], "medium")

    def test_resolve_llm_selection_uses_default_effort_model(self):
        with patch.dict(
            os.environ,
            {
                "LLM_PROVIDER": "claude",
                "DEFAULT_MODEL_LOW": "claude-haiku-4-5",
                "DEFAULT_MODEL_MEDIUM": "claude-sonnet-4-5",
            },
            clear=False,
        ):
            importlib.reload(rag_pipeline)
            selection = rag_pipeline.resolve_llm_selection(effort="medium")

        self.assertEqual(selection["provider"], "claude")
        self.assertEqual(selection["model"], "claude-sonnet-4-5")
        self.assertEqual(selection["effort"], "medium")

    def test_resolve_llm_selection_uses_provider_specific_effort_model(self):
        with patch.dict(
            os.environ,
            {
                "LLM_PROVIDER": "claude",
                "DEFAULT_MODEL_LOW": "claude-haiku-4-5",
                "DEFAULT_MODEL_MEDIUM": "claude-sonnet-4-5",
                "OPENAI_MODEL_LOW": "gpt-4.1-mini",
                "OPENAI_MODEL_MEDIUM": "gpt-4.1",
            },
            clear=False,
        ):
            importlib.reload(rag_pipeline)
            selection = rag_pipeline.resolve_llm_selection(
                provider="openai",
                effort="medium",
            )

        self.assertEqual(selection["provider"], "openai")
        self.assertEqual(selection["model"], "gpt-4.1")
        self.assertEqual(selection["effort"], "medium")
