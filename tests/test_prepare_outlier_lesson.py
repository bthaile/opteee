import tempfile
import unittest
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from scripts.prepare_outlier_lesson import (
    LessonHistory,
    TopicCandidate,
    choose_candidate_topics,
    load_recent_history,
    select_source_pair,
    validate_raw_source,
)


EXCERPT = (
    "A trader should define the portfolio objective and maximum planned loss before "
    "opening the position. The transcript then explains how repeatable sizing and a "
    "specific invalidation trigger make later review useful instead of relying on a "
    "vague memory of the setup or its outcome."
)


def source(video_id="abcDEF123_-", timestamp=82, **updates):
    value = {
        "source_type": "video",
        "title": "How to Build a Repeatable Options Trade Process",
        "video_url_with_timestamp": f"https://www.youtube.com/watch?v={video_id}&t={timestamp}",
        "start_timestamp_seconds": timestamp,
        "start_timestamp": "1:22",
        "excerpt": EXCERPT,
    }
    value.update(updates)
    return value


class CitationAcceptanceTests(unittest.TestCase):
    def test_accepts_complete_video_citation(self):
        self.assertEqual(validate_raw_source(source()), (True, "accepted"))

    def test_accepts_content_as_excerpt_fallback(self):
        item = source()
        item["content"] = item.pop("excerpt")
        self.assertTrue(validate_raw_source(item)[0])

    def test_rejects_each_required_invalid_field(self):
        cases = {
            "pdf": {"source_type": "pdf"},
            "id title": {"title": "abcDEF123_-"},
            "generic ID title": {"title": "Video abcDEF123_-"},
            "unknown title": {"title": "Unknown Title"},
            "zero seconds": {"start_timestamp_seconds": 0},
            "non-clock timestamp": {"start_timestamp": "82 seconds"},
            "http URL": {"video_url_with_timestamp": "http://www.youtube.com/watch?v=abcDEF123_-&t=82"},
            "non-watch URL": {"video_url_with_timestamp": "https://youtu.be/abcDEF123_-?t=82"},
            "missing t": {"video_url_with_timestamp": "https://www.youtube.com/watch?v=abcDEF123_-"},
            "zero t": {"video_url_with_timestamp": "https://www.youtube.com/watch?v=abcDEF123_-&t=0"},
            "thin excerpt": {"excerpt": "A few words are not meaningful evidence."},
            "repetitive excerpt": {"excerpt": "trade risk " * 30},
        }
        for label, update in cases.items():
            with self.subTest(label=label):
                accepted, reason = validate_raw_source(source(**update))
                self.assertFalse(accepted)
                self.assertNotEqual(reason, "accepted")


class SourcePairTests(unittest.TestCase):
    def test_dedupes_citations_and_selects_distinct_videos(self):
        first = source(video_id="firstVID001", timestamp=82)
        duplicate = dict(first)
        same_video_later = source(video_id="firstVID001", timestamp=140, start_timestamp="2:20")
        second = source(video_id="secondVID02", timestamp=95, start_timestamp="1:35")

        pair, rejected = select_source_pair([first, duplicate, same_video_later, second])

        self.assertEqual([item["video_id"] for item in pair], ["firstVID001", "secondVID02"])
        self.assertEqual(rejected["duplicate citation in API response"], 1)

    def test_prefers_videos_not_present_in_recent_history(self):
        recent = source(video_id="recentVID01", timestamp=60, start_timestamp="1:00")
        novel_one = source(video_id="novelVID001", timestamp=70, start_timestamp="1:10")
        novel_two = source(video_id="novelVID002", timestamp=80, start_timestamp="1:20")

        pair, _ = select_source_pair([recent, novel_one, novel_two], {"recentVID01"})

        self.assertEqual([item["video_id"] for item in pair], ["novelVID001", "novelVID002"])

    def test_fails_when_only_one_distinct_video_is_valid(self):
        pair, rejected = select_source_pair(
            [source(timestamp=82), source(timestamp=140, start_timestamp="2:20")]
        )
        self.assertIsNone(pair)
        self.assertEqual(rejected["fewer than two distinct accepted videos"], 1)

    def test_topic_anchor_excludes_structurally_valid_off_topic_sources(self):
        topic = TopicCandidate(
            "strategy",
            "volatility risk premium",
            "Compare implied and realized volatility",
            "volatility evidence",
        )
        off_topic = source(video_id="offtopic001", excerpt=EXCERPT)
        implied = source(
            video_id="impliedV001",
            excerpt=EXCERPT + " Implied volatility can remain above subsequent realized volatility.",
        )
        realized = source(
            video_id="realized001",
            excerpt=EXCERPT + " Compare realized volatility with implied volatility before selling premium.",
        )

        pair, rejected = select_source_pair([off_topic, implied, realized], topic=topic)

        self.assertEqual([item["video_id"] for item in pair], ["realized001", "impliedV001"])
        self.assertEqual(rejected["source has no deterministic topic anchor"], 1)


class HistoryDedupeTests(unittest.TestCase):
    def test_reads_only_dated_markdown_in_fourteen_day_window(self):
        today = date(2026, 9, 8)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recent = root / today.isoformat()
            recent.with_suffix(".md").write_text(
                "Topic Bucket: position sizing\n"
                "Concept: Size from planned loss before entry.\n"
                "https://www.youtube.com/watch?v=abcDEF123_-&t=82\n",
                encoding="utf-8",
            )
            (root / f"{today - timedelta(days=14)}.md").write_text(
                "Topic Bucket: too old\nConcept: Ignore me.\n", encoding="utf-8"
            )
            (root / "notes.md").write_text("Topic Bucket: undated\n", encoding="utf-8")

            history = load_recent_history(root, today)

        self.assertEqual(history.buckets, ["position sizing"])
        self.assertEqual(history.concepts, ["Size from planned loss before entry."])
        self.assertEqual(history.video_ids, {"abcDEF123_-"})
        self.assertEqual(history.window_start, date(2026, 8, 26))

    def test_topic_choice_skips_recent_bucket(self):
        today = date(2026, 9, 8)
        history = LessonHistory(today - timedelta(days=13), today, [], ["position sizing"], [], set(), set())
        sizing = TopicCandidate("process", "position sizing", "Size the trade", "position sizing")
        exits = TopicCandidate("process", "exit planning", "Plan the exit", "exit planning")

        eligible, skipped = choose_candidate_topics(history, candidates=[sizing, exits])

        self.assertEqual(eligible, [exits])
        self.assertEqual(skipped, [sizing])


if __name__ == "__main__":
    unittest.main()
