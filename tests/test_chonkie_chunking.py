import unittest

from chonkie_chunking import chunk_transcript_segments_with_chonkie
from preprocess_transcripts import create_chunks


class ChonkieTranscriptChunkingTests(unittest.TestCase):
    def test_chonkie_transcript_chunking_preserves_timestamp_ranges(self):
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

    def test_create_chunks_falls_back_for_tiny_transcripts(self):
        segments = [
            {"timestamp": 0.0, "text": "tiny"},
            {"timestamp": 5.0, "text": "clip words"},
        ]

        chunks = create_chunks(segments, chunk_size=250, overlap=50, min_words=10)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["word_count"], 3)
        self.assertEqual(chunks[0]["start_timestamp_seconds"], 0.0)
        self.assertEqual(chunks[0]["end_timestamp_seconds"], 5.0)


if __name__ == "__main__":
    unittest.main()
