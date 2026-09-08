"""Repair and preserve source metadata for processed YouTube transcripts."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence

YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
PLACEHOLDER_TITLES = {
    "no title",
    "unknown",
    "unknown title",
    "untitled",
}


def is_bare_youtube_id_title(title: object, video_id: object | None = None) -> bool:
    """Return whether *title* is just a YouTube ID (optionally the expected ID)."""
    if not isinstance(title, str):
        return False
    candidate = title.strip()
    if not YOUTUBE_ID_RE.fullmatch(candidate):
        return False
    if video_id is None:
        return True
    return isinstance(video_id, str) and candidate == video_id.strip()


def is_human_readable_title(title: object, video_id: object | None = None) -> bool:
    """Return whether a title is safe to prefer over an ID/placeholder."""
    if not isinstance(title, str) or not title.strip():
        return False
    candidate = title.strip()
    return (
        candidate.casefold() not in PLACEHOLDER_TITLES
        and not is_bare_youtube_id_title(candidate, video_id)
    )


def load_metadata_records(paths: Iterable[Path | str]) -> list[dict]:
    """Load and combine metadata arrays, retaining the best record per video ID."""
    combined: list[dict] = []
    by_id: dict[str, dict] = {}
    for path_value in paths:
        path = Path(path_value)
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as handle:
            records = json.load(handle)
        if not isinstance(records, list):
            raise ValueError(f"Metadata file must contain a JSON array: {path}")
        for record in records:
            if not isinstance(record, dict):
                continue
            video_id = record.get("video_id") or record.get("id")
            if not isinstance(video_id, str) or not video_id:
                continue
            normalized = dict(record)
            normalized["video_id"] = video_id
            if video_id not in by_id:
                by_id[video_id] = normalized
                combined.append(normalized)
                continue
            current = by_id[video_id]
            for key, value in normalized.items():
                if value is not None and current.get(key) in (None, ""):
                    current[key] = value
            if is_human_readable_title(
                normalized.get("title"), video_id
            ) and not is_human_readable_title(current.get("title"), video_id):
                current["title"] = normalized["title"].strip()
    return combined


def merge_video_metadata(
    existing: Sequence[Mapping], incoming: Sequence[Mapping]
) -> list[dict]:
    """Merge a fresh scrape with history without downgrading titles or dropping IDs."""
    existing_by_id = {
        item.get("video_id"): dict(item)
        for item in existing
        if isinstance(item, Mapping) and item.get("video_id")
    }
    merged: list[dict] = []
    seen: set[str] = set()

    for item in incoming:
        video_id = item.get("video_id")
        if not video_id:
            continue
        record = dict(existing_by_id.get(video_id, {}))
        old_title = record.get("title")
        record.update({key: value for key, value in item.items() if value is not None})
        if is_human_readable_title(old_title, video_id) and not is_human_readable_title(
            item.get("title"), video_id
        ):
            record["title"] = old_title
        merged.append(record)
        seen.add(video_id)

    merged.extend(
        record for video_id, record in existing_by_id.items() if video_id not in seen
    )
    return merged


def fetch_metadata_with_ytdlp(video_id: str) -> dict | None:
    """Fetch one video's metadata without downloading media."""
    import yt_dlp

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as exc:
        print(f"  warning: yt-dlp metadata lookup failed for {video_id}: {exc}")
        return None
    if not isinstance(info, dict) or not is_human_readable_title(
        info.get("title"), video_id
    ):
        return None
    return {
        "video_id": video_id,
        "title": info["title"].strip(),
        "url": info.get("webpage_url") or url,
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "description": info.get("description"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
    }


def _atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode if path.exists() else None
    temporary_name = ""
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as handle:
            temporary_name = handle.name
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        if mode is not None:
            os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _metadata_lookup(records: Sequence[Mapping]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for record in records:
        video_id = record.get("video_id")
        if isinstance(video_id, str) and is_human_readable_title(
            record.get("title"), video_id
        ):
            result[video_id] = dict(record)
    return result


def _upsert_fetched_metadata(
    records: Sequence[Mapping], fetched: Mapping
) -> list[dict]:
    """Add fetched fields while preserving any existing human-authored title."""
    video_id = fetched["video_id"]
    result = [dict(record) for record in records]
    for record in result:
        if record.get("video_id") != video_id:
            continue
        current_title = record.get("title")
        record.update(
            {key: value for key, value in fetched.items() if value is not None}
        )
        if is_human_readable_title(current_title, video_id):
            record["title"] = current_title
        return result
    result.append(dict(fetched))
    return result


def _enrich_chunk(chunk: dict, video_id: str, metadata: Mapping) -> bool:
    """Apply only quality-improving source fields to a matching chunk."""
    if chunk.get("video_id") != video_id:
        return False
    changed = False
    title = metadata.get("title")
    if is_bare_youtube_id_title(
        chunk.get("title"), video_id
    ) and is_human_readable_title(title, video_id):
        chunk["title"] = title.strip()
        changed = True

    source_fields = {
        "upload_date": metadata.get("upload_date"),
        "published_at": metadata.get("published_at") or metadata.get("publishedAt"),
        "duration": metadata.get("duration"),
    }
    for field, value in source_fields.items():
        if chunk.get(field) in (None, "") and value not in (None, ""):
            chunk[field] = value
            changed = True
    return changed


def repair_processed_transcript_metadata(
    processed_dir: Path,
    metadata_paths: Sequence[Path],
    *,
    allow_network: bool = True,
    dry_run: bool = False,
    video_ids: set[str] | None = None,
    fetcher: Callable[[str], dict | None] = fetch_metadata_with_ytdlp,
) -> dict[str, int]:
    """Repair ID-only chunk titles from canonical metadata, then yt-dlp.

    Only chunks whose title exactly matches their own valid YouTube ID are changed.
    Consequently a human-readable existing title is never overwritten.
    """
    metadata_records = load_metadata_records(metadata_paths)
    canonical = _metadata_lookup(metadata_records)
    candidates: dict[str, list[tuple[Path, list[dict]]]] = {}
    invalid_files = 0

    for path in sorted(processed_dir.glob("*_processed.json")):
        try:
            with path.open(encoding="utf-8") as handle:
                chunks = json.load(handle)
        except (OSError, json.JSONDecodeError):
            invalid_files += 1
            continue
        if not isinstance(chunks, list) or not all(
            isinstance(chunk, dict) for chunk in chunks
        ):
            invalid_files += 1
            continue
        affected_ids = {
            chunk.get("video_id")
            for chunk in chunks
            if is_bare_youtube_id_title(chunk.get("title"), chunk.get("video_id"))
        }
        for video_id in affected_ids:
            if video_ids is None or video_id in video_ids:
                candidates.setdefault(video_id, []).append((path, chunks))

    fetched_by_id: dict[str, dict] = {}
    unresolved = 0
    files_changed = 0
    chunks_changed = 0

    for video_id, files in candidates.items():
        replacement = canonical.get(video_id)
        if replacement is None and allow_network:
            replacement = fetcher(video_id)
            if replacement and is_human_readable_title(
                replacement.get("title"), video_id
            ):
                replacement = dict(replacement)
                replacement["video_id"] = video_id
                fetched_by_id[video_id] = replacement
        if replacement is None or not is_human_readable_title(
            replacement.get("title"), video_id
        ):
            unresolved += 1
            continue

        for path, chunks in files:
            changed = 0
            for chunk in chunks:
                if _enrich_chunk(chunk, video_id, replacement):
                    changed += 1
            if changed:
                files_changed += 1
                chunks_changed += changed
                if not dry_run:
                    _atomic_write_json(path, chunks)

    if fetched_by_id and not dry_run:
        for path in metadata_paths:
            records = load_metadata_records([path]) if path.exists() else []
            for fetched in fetched_by_id.values():
                records = _upsert_fetched_metadata(records, fetched)
            _atomic_write_json(path, records)

    return {
        "affected_videos": len(candidates),
        "repaired_videos": len(candidates) - unresolved,
        "fetched_videos": len(fetched_by_id),
        "unresolved_videos": unresolved,
        "files_changed": files_changed,
        "chunks_changed": chunks_changed,
        "invalid_files": invalid_files,
    }
