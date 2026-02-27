import unittest

from app.services.history_utils import sanitize_history_content


class HistoryUtilsTests(unittest.TestCase):
    def test_sanitize_history_content_removes_reference_markup_for_assistant(self):
        raw = (
            "### Answer\nA concise response"
            "<div class=\"video-references-section\">"
            "<div class='source-ref-block'>cards</div>"
            "</div>"
        )
        sanitized = sanitize_history_content("assistant", raw)

        self.assertEqual(sanitized, "Answer A concise response")
        self.assertNotIn("video-references-section", sanitized)
        self.assertNotIn("<div", sanitized)

    def test_sanitize_history_content_keeps_user_content_intact(self):
        content = "<div>user asked this</div>"
        self.assertEqual(sanitize_history_content("user", content), content)

