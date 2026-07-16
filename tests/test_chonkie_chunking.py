import unittest

from chonkie_chunking import (
    chunk_pdf_elements_with_chonkie,
    chunk_transcript_segments_with_chonkie,
)


class ChonkieChunkingTests(unittest.TestCase):
    def test_transcript_chunking_preserves_timestamp_ranges(self):
        segments = [
            {"timestamp": 0.0, "text": "First segment about portfolio risk and sizing."},
            {"timestamp": 15.0, "text": "Second segment about delta exposure and correlation."},
            {"timestamp": 32.0, "text": "Third segment about exits and trade management."},
        ]

        chunks = chunk_transcript_segments_with_chonkie(
            segments,
            chunk_size=8,
            overlap=2,
            min_words=3,
        )

        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0]["start_timestamp_seconds"], 0.0)
        self.assertGreaterEqual(chunks[-1]["end_timestamp_seconds"], 15.0)
        self.assertTrue(all(chunk["word_count"] >= 3 for chunk in chunks))
        self.assertTrue(all(chunk["end_char"] > chunk["start_char"] for chunk in chunks))

    def test_pdf_chunking_preserves_pages_and_section(self):
        elements = [
            {"type": "section", "text": "Risk Management", "page": 1},
            {"type": "paragraph", "text": "Keep position size small when volatility expands and portfolio correlation rises.", "page": 1},
            {"type": "paragraph", "text": "Use defined exits and avoid oversized premium relative to account risk.", "page": 2},
        ]

        chunks = chunk_pdf_elements_with_chonkie(
            elements,
            target_size=10,
            overlap=2,
            min_words=3,
        )

        self.assertGreaterEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["section"], "Risk Management")
        self.assertIn(1, chunks[0]["pages"])
        self.assertTrue(all(chunk["word_count"] >= 3 for chunk in chunks))
        self.assertTrue(all(chunk["end_char"] > chunk["start_char"] for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
