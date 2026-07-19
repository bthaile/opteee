from __future__ import annotations

from dataclasses import dataclass

from chonkie import Document, SentenceChunker

DEFAULT_DELIMS = [". ", "! ", "? ", "\n\n", "\n"]


@dataclass
class SpanRecord:
    start: int
    end: int
    payload: dict


class OpteeeSentenceChunker:
    def __init__(self, chunk_size: int, chunk_overlap: int) -> None:
        self.chunker = SentenceChunker(
            tokenizer="word",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_sentences_per_chunk=1,
            min_characters_per_sentence=1,
            delim=DEFAULT_DELIMS,
            include_delim="prev",
        )

    def chunk(self, text: str, metadata: dict | None = None):
        document = Document(content=text, metadata=metadata or {})
        return self.chunker.chunk_document(document).chunks


def _normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def _overlapping_payloads(records: list[SpanRecord], start: int, end: int) -> list[dict]:
    overlaps: list[dict] = []
    for record in records:
        if record.end <= start:
            continue
        if record.start >= end:
            break
        overlaps.append(record.payload)
    return overlaps


def chunk_transcript_segments_with_chonkie(
    segments: list[dict],
    chunk_size: int,
    overlap: int,
    min_words: int,
) -> list[dict]:
    if not segments:
        return []

    pieces: list[str] = []
    spans: list[SpanRecord] = []
    cursor = 0
    for idx, segment in enumerate(segments):
        text = _normalize_text(segment.get("text", ""))
        if not text:
            continue
        prefix = "\n" if pieces else ""
        if prefix:
            pieces.append(prefix)
            cursor += len(prefix)
        start = cursor
        pieces.append(text)
        cursor += len(text)
        spans.append(
            SpanRecord(
                start=start,
                end=cursor,
                payload={
                    "timestamp": float(segment.get("timestamp", 0.0)),
                    "segment_index": idx,
                },
            )
        )

    text = "".join(pieces)
    if not text:
        return []

    chunker = OpteeeSentenceChunker(chunk_size=chunk_size, chunk_overlap=overlap)
    raw_chunks = chunker.chunk(text)
    chunks: list[dict] = []
    for chunk_index, chunk in enumerate(raw_chunks):
        chunk_text = _normalize_text(chunk.text)
        word_count = len(chunk_text.split())
        if word_count < min_words:
            continue
        overlaps = _overlapping_payloads(spans, chunk.start_index, chunk.end_index)
        if not overlaps:
            continue
        chunks.append(
            {
                "text": chunk_text,
                "start_timestamp_seconds": overlaps[0]["timestamp"],
                "end_timestamp_seconds": overlaps[-1]["timestamp"],
                "word_count": word_count,
                "chunk_index": chunk_index,
                "start_char": chunk.start_index,
                "end_char": chunk.end_index,
                "token_count": chunk.token_count,
            }
        )
    return chunks
