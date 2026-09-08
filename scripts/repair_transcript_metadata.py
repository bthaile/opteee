#!/usr/bin/env python3
"""Repair ID-only titles in processed transcript chunks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline_config import METADATA_JSON, PROCESSED_DIR
from transcript_metadata import repair_processed_transcript_metadata


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair bare YouTube-ID titles without re-chunking or rebuilding vectors."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report repairs without writing files"
    )
    parser.add_argument(
        "--no-network", action="store_true", help="Use canonical metadata only"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any affected title remains unresolved",
    )
    parser.add_argument(
        "--video-id", action="append", dest="video_ids", help="Limit repair to an ID"
    )
    args = parser.parse_args()

    stats = repair_processed_transcript_metadata(
        ROOT / PROCESSED_DIR,
        [ROOT / METADATA_JSON],
        allow_network=not args.no_network,
        dry_run=args.dry_run,
        video_ids=set(args.video_ids) if args.video_ids else None,
    )
    action = "Would repair" if args.dry_run else "Repaired"
    print(
        f"{action} {stats['chunks_changed']} chunks in {stats['files_changed']} files "
        f"across {stats['repaired_videos']} videos "
        f"({stats['fetched_videos']} fetched, {stats['unresolved_videos']} unresolved)."
    )
    if stats["invalid_files"]:
        print(
            f"warning: skipped {stats['invalid_files']} malformed processed transcript files"
        )
    return (
        1
        if args.strict and (stats["unresolved_videos"] or stats["invalid_files"])
        else 0
    )


if __name__ == "__main__":
    raise SystemExit(main())
