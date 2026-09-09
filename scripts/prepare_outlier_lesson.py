#!/usr/bin/env python3
"""Prepare deterministic source inputs for the Outlier daily lesson generator.

This program only reads lesson history, queries OPTEEE, and writes one JSON
artifact.  It deliberately does not generate or deliver a lesson.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


DEFAULT_HISTORY_DIR = Path("/Users/bradfordhaile/clawd/reports/trading-education")
DEFAULT_ENDPOINT = "http://127.0.0.1:7860/api/chat"
REPORT_TIMEZONE = ZoneInfo("America/Chicago")
HISTORY_DAYS = 14
MAX_QUERIES_LIMIT = 8
MAX_RESULTS_LIMIT = 20
MAX_RESPONSE_BYTES = 2_000_000
MIN_EXCERPT_CHARS = 120
MIN_EXCERPT_WORDS = 20
MIN_UNIQUE_EXCERPT_WORDS = 12

_CLOCK_RE = re.compile(r"^(?:\d+:[0-5]\d|\d+:[0-5]\d:[0-5]\d)$")
_YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_UUID_OR_HASH_RE = re.compile(
    r"^(?:[0-9a-f]{8}-[0-9a-f-]{27,}|[0-9a-f]{20,}|\d{8,})$", re.IGNORECASE
)
_URL_RE = re.compile(r"https://(?:www\.)?youtube\.com/watch\?[^\s)>\"'`]+")
_WORD_RE = re.compile(r"[a-z0-9]+")
_STOP_WORDS = {
    "a", "an", "and", "as", "at", "before", "by", "for", "from", "in",
    "into", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "use", "with", "your",
}


@dataclass(frozen=True)
class TopicCandidate:
    category: str
    bucket: str
    concept: str
    query: str


@dataclass
class LessonHistory:
    window_start: date
    window_end: date
    files: List[str]
    buckets: List[str]
    concepts: List[str]
    video_ids: Set[str]
    citation_keys: Set[Tuple[str, int]]


TOPIC_CANDIDATES: Tuple[TopicCandidate, ...] = (
    TopicCandidate("process", "trade hypothesis", "Write a falsifiable trade thesis before choosing a structure", "Outlier process for writing and falsifying a trade thesis before selecting an options structure"),
    TopicCandidate("strategy", "vertical spread construction", "Choose vertical-spread width from the payoff objective, not premium alone", "Outlier strategy guidance for choosing vertical spread width, risk, and payoff tradeoffs"),
    TopicCandidate("process", "position sizing", "Size from the planned loss and portfolio risk budget before entry", "Outlier process for stop-based position sizing and portfolio risk budgeting before entry"),
    TopicCandidate("strategy", "calendar spreads", "Match a calendar spread to the expected timing of the move and volatility change", "Outlier strategy guidance on calendar spreads, timing, term structure, and volatility"),
    TopicCandidate("process", "exit planning", "Define the evidence that closes a trade before the position is opened", "Outlier process for defining invalidation, profit taking, and exits before trade entry"),
    TopicCandidate("strategy", "covered calls", "Treat a covered call as a capped-upside position with downside risk", "Outlier strategy guidance on covered calls, capped upside, assignment, and downside risk"),
    TopicCandidate("process", "portfolio correlation", "Check shared factor exposure before counting positions as diversified", "Outlier process for checking portfolio correlation, concentration, and shared factor exposure"),
    TopicCandidate("strategy", "iron condors", "Set iron-condor wings and size from the loss scenario, not win rate", "Outlier strategy guidance on iron condor construction, wing width, sizing, and loss scenarios"),
    TopicCandidate("process", "trade management", "Tie each adjustment to a predeclared trigger and portfolio objective", "Outlier process for rule-based trade adjustments and portfolio-aware management triggers"),
    TopicCandidate("strategy", "earnings volatility", "Separate the earnings move forecast from the implied-volatility forecast", "Outlier strategy guidance on earnings trades, expected moves, and implied volatility crush"),
    TopicCandidate("process", "sample size", "Set the review sample size before judging whether an edge persists", "Outlier process for sample size, avoiding overfitting, and evaluating whether an edge persists"),
    TopicCandidate("strategy", "ratio spreads", "Evaluate ratio spreads by their tail exposure rather than the entry credit", "Outlier strategy guidance on ratio spreads, tail risk, and expiration payoff exposure"),
    TopicCandidate("process", "execution quality", "Measure slippage separately from whether the trade thesis worked", "Outlier process for measuring execution quality, fills, slippage, and thesis performance separately"),
    TopicCandidate("strategy", "volatility risk premium", "Demand evidence that implied volatility is rich relative to the risk being sold", "Outlier strategy guidance on volatility risk premium and comparing implied with realized volatility"),
    TopicCandidate("process", "scenario planning", "Write the position response to up, down, and unchanged markets before entry", "Outlier process for scenario analysis across up, down, and unchanged market paths"),
    TopicCandidate("strategy", "diagonal spreads", "Separate directional exposure from term-structure exposure in a diagonal", "Outlier strategy guidance on diagonal spreads, directional exposure, and volatility term structure"),
)

# At least one topic-specific anchor must occur in a source title/excerpt.  This
# prevents a structurally valid but off-topic retrieval from becoming evidence.
TOPIC_ANCHORS: Dict[str, Tuple[str, ...]] = {
    "trade hypothesis": ("trade thesis", "hypothesis", "falsif", "invalidation"),
    "vertical spread construction": ("vertical spread", "spread width", "width of the spread"),
    "position sizing": ("position sizing", "size the position", "max loss", "risk per trade"),
    "calendar spreads": ("calendar spread", "time spread", "term structure"),
    "exit planning": ("exit plan", "exit criteria", "invalidation", "profit target"),
    "covered calls": ("covered call", "capped upside", "assignment"),
    "portfolio correlation": ("correlation", "correlated", "concentration", "factor exposure"),
    "iron condors": ("iron condor", "wing width"),
    "trade management": ("management trigger", "adjustment trigger", "trade management"),
    "earnings volatility": ("earnings", "volatility crush", "expected move"),
    "sample size": ("sample size", "observations", "overfitting"),
    "ratio spreads": ("ratio spread", "backspread", "tail risk", "unlimited risk"),
    "execution quality": ("slippage", "fill quality", "execution quality", "bid ask"),
    "volatility risk premium": ("volatility risk premium", "implied volatility", "realized volatility"),
    "scenario planning": ("scenario analysis", "scenario planning", "if the market", "market moves"),
    "diagonal spreads": ("diagonal spread", "diagonal", "term structure"),
}


def _tokens(value: str) -> Set[str]:
    return {word for word in _WORD_RE.findall(value.lower()) if word not in _STOP_WORDS and len(word) > 1}


def concepts_overlap(candidate: TopicCandidate, recent_buckets: Iterable[str], recent_concepts: Iterable[str]) -> bool:
    """Return True when a candidate materially repeats a recent bucket/concept."""
    candidate_bucket = " ".join(candidate.bucket.lower().split())
    candidate_tokens = _tokens(f"{candidate.bucket} {candidate.concept}")
    for bucket in recent_buckets:
        normalized = " ".join(bucket.lower().split())
        if normalized and (normalized == candidate_bucket or normalized in candidate_bucket or candidate_bucket in normalized):
            return True
    for concept in recent_concepts:
        recent_tokens = _tokens(concept)
        shared = candidate_tokens & recent_tokens
        if len(shared) >= 2 and len(shared) / max(1, min(len(candidate_tokens), len(recent_tokens))) >= 0.40:
            return True
    return False


def choose_candidate_topics(
    history: LessonHistory,
    *,
    candidates: Sequence[TopicCandidate] = TOPIC_CANDIDATES,
) -> Tuple[List[TopicCandidate], List[TopicCandidate]]:
    """Return eligible and skipped topics in a date-rotated deterministic order."""
    if not candidates:
        return [], []
    offset = history.window_end.toordinal() % len(candidates)
    ordered = list(candidates[offset:]) + list(candidates[:offset])
    eligible, skipped = [], []
    for candidate in ordered:
        target = skipped if concepts_overlap(candidate, history.buckets, history.concepts) else eligible
        target.append(candidate)
    return eligible, skipped


def _youtube_identity(url: str) -> Optional[Tuple[str, int]]:
    try:
        parsed = urlparse(url)
    except (TypeError, ValueError):
        return None
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        return None
    if parsed.path != "/watch":
        return None
    query = parse_qs(parsed.query)
    video_id = query.get("v", [""])[0]
    timestamp = query.get("t", [""])[0]
    if not _YOUTUBE_ID_RE.fullmatch(video_id):
        return None
    match = re.fullmatch(r"(\d+)s?", timestamp)
    if not match or int(match.group(1)) <= 0:
        return None
    return video_id, int(match.group(1))


def validate_raw_source(source: Mapping[str, Any]) -> Tuple[bool, str]:
    """Apply the complete deterministic citation acceptance contract."""
    if source.get("source_type") != "video":
        return False, "source_type is not video"

    title = " ".join(str(source.get("title") or "").split())
    title_words = re.findall(r"[A-Za-z][A-Za-z0-9'’-]*", title)
    title_without_id = re.sub(r"[A-Za-z0-9_-]{11}", " ", title).lower()
    residual_words = set(_WORD_RE.findall(title_without_id))
    if (
        len(title) < 8
        or len(title_words) < 2
        or title.lower() in {"unknown", "untitled", "video", "none", "n/a"}
        or title.lower().startswith(("unknown title", "untitled video"))
        or _YOUTUBE_ID_RE.fullmatch(title)
        or _UUID_OR_HASH_RE.fullmatch(title)
        or (
            re.search(r"(?:^|\s)[A-Za-z0-9_-]{11}(?:\s|$)", title)
            and residual_words <= {"video", "youtube", "source", "transcript", "id"}
        )
    ):
        return False, "title is missing, generic, or ID-like"

    seconds = source.get("start_timestamp_seconds")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds <= 0:
        return False, "start_timestamp_seconds is not a positive number"

    clock = str(source.get("start_timestamp") or source.get("timestamp") or "").strip()
    if not _CLOCK_RE.fullmatch(clock):
        return False, "start_timestamp is not clock-form"

    timestamp_url = str(source.get("video_url_with_timestamp") or "").strip()
    if _youtube_identity(timestamp_url) is None:
        return False, "video_url_with_timestamp is not an HTTPS YouTube watch URL with positive t="

    excerpt = " ".join(str(source.get("excerpt") or source.get("content") or "").split())
    excerpt_words = _WORD_RE.findall(excerpt.lower())
    if (
        len(excerpt) < MIN_EXCERPT_CHARS
        or len(excerpt_words) < MIN_EXCERPT_WORDS
        or len(set(excerpt_words)) < MIN_UNIQUE_EXCERPT_WORDS
    ):
        return False, "excerpt is not materially nontrivial"
    return True, "accepted"


def normalize_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    """Keep only lesson-preparation fields in a stable shape."""
    url = str(source["video_url_with_timestamp"]).strip()
    identity = _youtube_identity(url)
    assert identity is not None
    excerpt = " ".join(str(source.get("excerpt") or source.get("content") or "").split())
    return {
        "title": " ".join(str(source["title"]).split()),
        "source_type": "video",
        "video_id": identity[0],
        "video_url_with_timestamp": url,
        "start_timestamp_seconds": source["start_timestamp_seconds"],
        "start_timestamp": str(source.get("start_timestamp") or source.get("timestamp")).strip(),
        "excerpt": excerpt,
    }


def source_relevance_score(source: Mapping[str, Any], topic: TopicCandidate) -> int:
    """Score lexical topic evidence without asking an LLM to judge relevance."""
    haystack = " ".join(
        str(source.get(field) or "") for field in ("title", "excerpt", "content")
    ).lower()
    haystack = " ".join(haystack.split())
    shared_tokens = _tokens(f"{topic.bucket} {topic.concept}") & _tokens(haystack)
    anchors = TOPIC_ANCHORS.get(topic.bucket, ())
    anchor_hits = sum(1 for anchor in anchors if anchor in haystack)
    if anchors and not anchor_hits:
        return 0
    if not anchors and len(shared_tokens) < 2:
        return 0
    return anchor_hits * 100 + len(shared_tokens)


def select_source_pair(
    raw_sources: Sequence[Mapping[str, Any]],
    recent_video_ids: Iterable[str] = (),
    topic: Optional[TopicCandidate] = None,
) -> Tuple[Optional[List[Dict[str, Any]]], Counter]:
    """Validate, dedupe, and select two distinct videos, preferring unused history."""
    rejected: Counter = Counter()
    accepted: List[Tuple[int, int, Dict[str, Any]]] = []
    seen_citations: Set[Tuple[str, int]] = set()
    for index, raw_source in enumerate(raw_sources):
        valid, reason = validate_raw_source(raw_source)
        if not valid:
            rejected[reason] += 1
            continue
        relevance = source_relevance_score(raw_source, topic) if topic else 0
        if topic and relevance <= 0:
            rejected["source has no deterministic topic anchor"] += 1
            continue
        source = normalize_source(raw_source)
        key = (source["video_id"], int(float(source["start_timestamp_seconds"])))
        if key in seen_citations:
            rejected["duplicate citation in API response"] += 1
            continue
        seen_citations.add(key)
        accepted.append((index, relevance, source))

    recent = set(recent_video_ids)
    accepted.sort(key=lambda item: (-item[1], item[2]["video_id"] in recent, item[0]))
    for first_index, (_, _, first) in enumerate(accepted):
        for _, _, second in accepted[first_index + 1 :]:
            if second["video_id"] != first["video_id"]:
                return [first, second], rejected
    rejected["fewer than two distinct accepted videos"] += 1
    return None, rejected


def load_recent_history(history_dir: Path, today: date) -> LessonHistory:
    if not history_dir.is_dir():
        raise RuntimeError(f"history directory does not exist: {history_dir}")
    window_start = today - timedelta(days=HISTORY_DAYS - 1)
    files: List[str] = []
    buckets: List[str] = []
    concepts: List[str] = []
    video_ids: Set[str] = set()
    citation_keys: Set[Tuple[str, int]] = set()
    for path in sorted(history_dir.rglob("*.md")):
        try:
            file_date = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if not window_start <= file_date <= today:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"cannot read history file {path}: {exc}") from exc
        files.append(str(path))
        buckets.extend(match.group(1).strip() for match in re.finditer(r"(?mi)^Topic Bucket:\s*(.+)$", text))
        concepts.extend(match.group(1).strip() for match in re.finditer(r"(?mi)^Concept:\s*(.+)$", text))
        for match in _URL_RE.finditer(text):
            identity = _youtube_identity(match.group(0))
            if identity:
                video_ids.add(identity[0])
                citation_keys.add(identity)
    return LessonHistory(window_start, today, files, buckets, concepts, video_ids, citation_keys)


def query_opteee(endpoint: str, topic: TopicCandidate, timeout: float, num_results: int) -> List[Mapping[str, Any]]:
    payload = json.dumps({"query": topic.query, "num_results": num_results, "format": "json"}).encode("utf-8")
    request = Request(endpoint, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(MAX_RESPONSE_BYTES + 1)
    except HTTPError as exc:
        detail = exc.read(500).decode("utf-8", errors="replace")
        raise RuntimeError(f"OPTEEE HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"OPTEEE request failed: {exc}") from exc
    if len(body) > MAX_RESPONSE_BYTES:
        raise RuntimeError(f"OPTEEE response exceeded {MAX_RESPONSE_BYTES} bytes")
    try:
        result = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"OPTEEE returned invalid JSON: {exc}") from exc
    raw_sources = result.get("raw_sources") if isinstance(result, dict) else None
    if not isinstance(raw_sources, list):
        raise RuntimeError("OPTEEE JSON response has no raw_sources list")
    return [item for item in raw_sources if isinstance(item, dict)]


def build_artifact(
    history: LessonHistory,
    topic: TopicCandidate,
    pair: List[Dict[str, Any]],
    *,
    queries_attempted: int,
    skipped_topics: Sequence[TopicCandidate],
    rejection_counts: Counter,
) -> Dict[str, Any]:
    reused = sorted({source["video_id"] for source in pair} & history.video_ids)
    return {
        "schema_version": 1,
        "selected_topic": {
            "category": topic.category,
            "bucket": topic.bucket,
            "concept": topic.concept,
            "query": topic.query,
        },
        "raw_sources": pair,
        "duplicate_history_summary": {
            "window_start": history.window_start.isoformat(),
            "window_end": history.window_end.isoformat(),
            "history_files": len(history.files),
            "recent_buckets": sorted(set(history.buckets)),
            "recent_concepts": sorted(set(history.concepts)),
            "recent_video_count": len(history.video_ids),
            "selected_recent_video_ids": reused,
            "candidate_topics_skipped": [candidate.concept for candidate in skipped_topics],
            "source_rejections": dict(sorted(rejection_counts.items())),
            "queries_attempted": queries_attempted,
        },
    }


def write_artifact(path: Path, artifact: Mapping[str, Any]) -> None:
    if not path.parent.is_dir():
        raise RuntimeError(f"output parent directory does not exist: {path.parent}")
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(artifact, handle, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except OSError as exc:
        if "temporary" in locals():
            temporary.unlink(missing_ok=True)
        raise RuntimeError(f"cannot write preparation artifact {path}: {exc}") from exc


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="path for the compact preparation JSON artifact")
    parser.add_argument("--history-dir", type=Path, default=DEFAULT_HISTORY_DIR)
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--max-queries", type=int, default=6)
    parser.add_argument("--num-results", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=45.0, help="per-request timeout in seconds")
    parser.add_argument("--today", type=date.fromisoformat, default=None, metavar="YYYY-MM-DD", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.max_queries <= MAX_QUERIES_LIMIT:
        parser.error(f"--max-queries must be between 1 and {MAX_QUERIES_LIMIT}")
    if not 2 <= args.num_results <= MAX_RESULTS_LIMIT:
        parser.error(f"--num-results must be between 2 and {MAX_RESULTS_LIMIT}")
    if not 0 < args.timeout <= 120:
        parser.error("--timeout must be greater than 0 and at most 120 seconds")
    parsed_endpoint = urlparse(args.endpoint)
    if parsed_endpoint.scheme not in {"http", "https"} or not parsed_endpoint.netloc:
        parser.error("--endpoint must be an absolute HTTP(S) URL")
    return args


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    today = args.today or datetime.now(REPORT_TIMEZONE).date()
    try:
        history = load_recent_history(args.history_dir, today)
        candidates, skipped = choose_candidate_topics(history)
        if not candidates:
            raise RuntimeError("all configured topic candidates duplicate concepts from the last 14 days")

        all_rejections: Counter = Counter()
        errors: List[str] = []
        attempts = 0
        for topic in candidates[: args.max_queries]:
            attempts += 1
            try:
                raw_sources = query_opteee(args.endpoint, topic, args.timeout, args.num_results)
            except RuntimeError as exc:
                errors.append(f"{topic.bucket}: {exc}")
                continue
            pair, rejected = select_source_pair(raw_sources, history.video_ids, topic)
            all_rejections.update(rejected)
            if pair is None:
                errors.append(f"{topic.bucket}: no pair of distinct valid video citations")
                continue
            artifact = build_artifact(
                history,
                topic,
                pair,
                queries_attempted=attempts,
                skipped_topics=skipped,
                rejection_counts=all_rejections,
            )
            write_artifact(args.output, artifact)
            print(f"prepared {args.output}: {topic.bucket}; 2 accepted sources after {attempts} query attempt(s)")
            return 0
        detail = "; ".join(errors) if errors else "no eligible candidate was queried"
        raise RuntimeError(f"no valid two-source candidate after {attempts} bounded query attempt(s): {detail}")
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
