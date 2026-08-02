"""
Automated Daily News Ingestion Scheduler
=========================================
Periodically collects news from RSS and NewsAPI (using API_KEY),
merges and deduplicates into SQLite, runs ML clustering/NER,
and updates the rolling intelligence timeline.

Usage:
    python -m backend.scheduler                   # Runs immediately, then every 6 hours
    python -m backend.scheduler --interval 12     # Runs immediately, then every 12 hours
    python -m backend.scheduler --no-immediate    # Waits for interval before first run
"""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
import time

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.pipeline import run_pipeline
from backend.utils.logger import logger


def execute_scheduled_job():
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    logger.info("=" * 60)
    logger.info("  [Scheduler] Starting scheduled news collection: %s", now_str)
    logger.info("=" * 60)

    try:
        run_pipeline(skip_collect=False, skip_ml=False)
        logger.info(
            "✓ [Scheduler] Pipeline completed successfully at %s",
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        )
    except Exception as e:
        logger.exception("❌ [Scheduler] Pipeline failed: %s", e)


def start_scheduler(interval_hours=6, run_immediately=True):
    logger.info("[Scheduler] NewsLens AI Ingestion Scheduler Started")
    logger.info("[Scheduler] Update interval: Every %d hours", interval_hours)

    if run_immediately:
        execute_scheduled_job()

    interval_seconds = interval_hours * 3600
    while True:
        logger.info("[Scheduler] Next pipeline run in %d hours...", interval_hours)
        time.sleep(interval_seconds)
        execute_scheduled_job()


def main():
    parser = argparse.ArgumentParser(description="Automated Daily News Ingestion Scheduler")
    parser.add_argument(
        "--interval",
        type=int,
        default=6,
        help="Interval between pipeline runs in hours (default: 6)",
    )
    parser.add_argument(
        "--no-immediate",
        action="store_true",
        help="Do not run pipeline immediately on startup",
    )
    args = parser.parse_args()

    try:
        start_scheduler(interval_hours=args.interval, run_immediately=not args.no_immediate)
    except KeyboardInterrupt:
        logger.info("\n[Scheduler] Scheduler stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
