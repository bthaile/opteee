import json
from pathlib import Path

from transcript_metadata import (
    is_bare_youtube_id_title,
    merge_video_metadata,
    repair_processed_transcript_metadata,
)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_bare_youtube_id_detection_is_strict():
    video_id = "AbC_12-xYz9"
    assert is_bare_youtube_id_title(video_id, video_id)
    assert is_bare_youtube_id_title(f" {video_id} ", video_id)
    assert not is_bare_youtube_id_title("A useful human title", video_id)
    assert not is_bare_youtube_id_title("too-short", "too-short")
    assert not is_bare_youtube_id_title("ZbC_12-xYz9", video_id)
    assert not is_bare_youtube_id_title(None, video_id)


def test_repair_prefers_canonical_title_and_preserves_human_title(tmp_path):
    video_id = "AbC_12-xYz9"
    processed = tmp_path / "processed"
    chunk_file = processed / f"{video_id}_processed.json"
    write_json(
        chunk_file,
        [
            {"video_id": video_id, "title": video_id, "text": "repair me"},
            {"video_id": video_id, "title": "Editor supplied title", "text": "keep me"},
        ],
    )
    metadata = tmp_path / "videos.json"
    write_json(
        metadata,
        [
            {
                "video_id": video_id,
                "title": "Canonical video title",
                "duration": 123,
            }
        ],
    )

    def unexpected_fetch(_video_id):
        raise AssertionError("canonical metadata should avoid a network lookup")

    stats = repair_processed_transcript_metadata(
        processed, [metadata], fetcher=unexpected_fetch
    )

    assert stats["chunks_changed"] == 2
    repaired_chunks = read_json(chunk_file)
    assert [chunk["title"] for chunk in repaired_chunks] == [
        "Canonical video title",
        "Editor supplied title",
    ]
    assert [chunk["duration"] for chunk in repaired_chunks] == [123, 123]
    assert [chunk["duration"] for chunk in read_json(chunk_file)] == [123, 123]


def test_repair_falls_back_to_ytdlp_metadata_and_is_idempotent(tmp_path):
    video_id = "AbC_12-xYz9"
    processed = tmp_path / "processed"
    chunk_file = processed / f"{video_id}_processed.json"
    write_json(chunk_file, [{"video_id": video_id, "title": video_id, "text": "text"}])
    metadata = tmp_path / "videos.json"
    write_json(metadata, [])
    calls = []

    def fetch(candidate):
        calls.append(candidate)
        return {
            "video_id": candidate,
            "title": "Fetched video title",
            "url": f"https://www.youtube.com/watch?v={candidate}",
        }

    first = repair_processed_transcript_metadata(processed, [metadata], fetcher=fetch)
    second = repair_processed_transcript_metadata(processed, [metadata], fetcher=fetch)

    assert first["fetched_videos"] == 1
    assert first["chunks_changed"] == 1
    assert second["affected_videos"] == 0
    assert second["chunks_changed"] == 0
    assert calls == [video_id]
    assert read_json(chunk_file)[0]["title"] == "Fetched video title"
    assert read_json(metadata)[0]["title"] == "Fetched video title"


def test_bad_fallback_cannot_replace_bare_title(tmp_path):
    video_id = "AbC_12-xYz9"
    processed = tmp_path / "processed"
    chunk_file = processed / f"{video_id}_processed.json"
    write_json(chunk_file, [{"video_id": video_id, "title": video_id}])

    stats = repair_processed_transcript_metadata(
        processed,
        [],
        fetcher=lambda candidate: {"video_id": candidate, "title": candidate},
    )

    assert stats["unresolved_videos"] == 1
    assert stats["chunks_changed"] == 0
    assert read_json(chunk_file)[0]["title"] == video_id


def test_malformed_processed_file_is_reported_and_skipped(tmp_path):
    processed = tmp_path / "processed"
    processed.mkdir()
    (processed / "broken_processed.json").write_text("{", encoding="utf-8")

    stats = repair_processed_transcript_metadata(processed, [], allow_network=False)

    assert stats["invalid_files"] == 1
    assert stats["chunks_changed"] == 0


def test_fresh_scrape_keeps_historical_records_and_never_downgrades_title():
    existing = [
        {"video_id": "AbC_12-xYz9", "title": "Good existing title", "duration": 10},
        {"video_id": "Old_12-xYz9", "title": "Historical title"},
    ]
    incoming = [{"video_id": "AbC_12-xYz9", "title": "AbC_12-xYz9", "duration": 11}]

    merged = merge_video_metadata(existing, incoming)

    assert merged == [
        {"video_id": "AbC_12-xYz9", "title": "Good existing title", "duration": 11},
        {"video_id": "Old_12-xYz9", "title": "Historical title"},
    ]
