"""
AI News Intelligence Pipeline
==============================
Single entry point that runs the entire NLP pipeline end-to-end:

    Step 1  ·  Collect RSS feeds
    Step 2  ·  Collect NewsAPI (optional — needs API_KEY)
    Step 3  ·  Merge & deduplicate into SQLite
    Step 4  ·  Generate sentence embeddings
    Step 5  ·  Agglomerative clustering
    Step 6  ·  Named Entity Recognition
    Step 7  ·  Generate event titles

Usage:
    python -m backend.pipeline                  # Full pipeline
    python -m backend.pipeline --skip-collect   # Re-process existing data (skip fetching)
    python -m backend.pipeline --skip-ml        # Collect only (skip ML steps)
"""

import argparse
import sys
import time
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.logger import logger


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _step_banner(step_number, total, label):
    """Print a clear step header."""
    bar = "─" * 50
    logger.info("")
    logger.info(bar)
    logger.info("  Step %d/%d — %s", step_number, total, label)
    logger.info(bar)


def _timed(func, *args, **kwargs):
    """Run a function and return (result, elapsed_seconds)."""
    start = time.time()
    result = func(*args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed


# ─────────────────────────────────────────────
# Pipeline steps
# ─────────────────────────────────────────────

def step_collect_rss():
    from backend.collectors.rss_collector import collect
    return collect()


def step_collect_newsapi():
    from backend.collectors.newsapi_collector import collect
    return collect()


def step_merge(rss_df, api_df):
    from backend.preprocessing.merge_dataset import main as merge_main
    merge_main(rss_df=rss_df, api_df=api_df)


def step_embeddings():
    from backend.embeddings.generate_embeddings import main as embed_main
    embed_main()


def step_clustering():
    from backend.clustering.agglomerative_clustering import main as cluster_main
    cluster_main()


def step_ner():
    from backend.ner.ner import main as ner_main
    ner_main()


def step_event_titles():
    from backend.summarization.generate_event_titles import main as titles_main
    titles_main()


# ─────────────────────────────────────────────
# Main pipeline
# ─────────────────────────────────────────────

def run_pipeline(skip_collect=False, skip_ml=False):
    """Execute the full AI News Intelligence pipeline."""

    total_steps = 7
    if skip_collect:
        total_steps -= 2
    if skip_ml:
        total_steps -= 4

    pipeline_start = time.time()
    step = 0
    timings = []

    logger.info("=" * 50)
    logger.info("  AI NEWS INTELLIGENCE PIPELINE")
    logger.info("  %s", "─" * 40)
    if skip_collect:
        logger.info("  ⚙  --skip-collect: Using existing data")
    if skip_ml:
        logger.info("  ⚙  --skip-ml: Collection only")
    logger.info("=" * 50)

    rss_df = None
    api_df = None

    # ── Collection Phase ──
    if not skip_collect:
        step += 1
        _step_banner(step, total_steps, "Collect RSS Feeds")
        rss_df, elapsed = _timed(step_collect_rss)
        timings.append(("RSS Collection", elapsed, len(rss_df) if rss_df is not None else 0))
        logger.info("✓ RSS collection done in %.1fs — %d articles", elapsed, len(rss_df) if rss_df is not None else 0)

        step += 1
        _step_banner(step, total_steps, "Collect NewsAPI (optional)")
        api_df, elapsed = _timed(step_collect_newsapi)
        article_count = len(api_df) if api_df is not None and not api_df.empty else 0
        timings.append(("NewsAPI Collection", elapsed, article_count))
        if article_count:
            logger.info("✓ NewsAPI done in %.1fs — %d articles", elapsed, article_count)
        else:
            logger.info("✓ NewsAPI skipped (no API key or no results)")

        # ── Merge Phase ──
        step += 1
        _step_banner(step, total_steps, "Merge & Deduplicate → SQLite")
        _, elapsed = _timed(step_merge, rss_df, api_df)
        timings.append(("Merge & Deduplicate", elapsed, None))
        logger.info("✓ Merge done in %.1fs", elapsed)
    else:
        logger.info("")
        logger.info("Skipping collection — using existing database.")

    # ── ML Phase ──
    if not skip_ml:
        step += 1
        _step_banner(step, total_steps, "Generate Sentence Embeddings")
        _, elapsed = _timed(step_embeddings)
        timings.append(("Embeddings", elapsed, None))
        logger.info("✓ Embeddings done in %.1fs", elapsed)

        step += 1
        _step_banner(step, total_steps, "Agglomerative Clustering")
        _, elapsed = _timed(step_clustering)
        timings.append(("Clustering", elapsed, None))
        logger.info("✓ Clustering done in %.1fs", elapsed)

        step += 1
        _step_banner(step, total_steps, "Named Entity Recognition")
        _, elapsed = _timed(step_ner)
        timings.append(("NER Extraction", elapsed, None))
        logger.info("✓ NER done in %.1fs", elapsed)

        step += 1
        _step_banner(step, total_steps, "Generate Event Titles")
        _, elapsed = _timed(step_event_titles)
        timings.append(("Event Titles", elapsed, None))
        logger.info("✓ Event titles done in %.1fs", elapsed)
    else:
        logger.info("")
        logger.info("Skipping ML pipeline — collection only mode.")

    # ── Summary ──
    total_elapsed = time.time() - pipeline_start
    logger.info("")
    logger.info("=" * 50)
    logger.info("  PIPELINE COMPLETE")
    logger.info("=" * 50)
    for name, elapsed, count in timings:
        extra = f" ({count} articles)" if count is not None else ""
        logger.info("  %-25s %6.1fs%s", name, elapsed, extra)
    logger.info("  %s", "─" * 40)
    logger.info("  %-25s %6.1fs", "TOTAL", total_elapsed)
    logger.info("=" * 50)
    logger.info("")
    logger.info("Your dashboard is ready! Start the API with:")
    logger.info("  uvicorn backend.api:app --reload")
    logger.info("")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI News Intelligence Pipeline — collect, process, and analyze news."
    )
    parser.add_argument(
        "--skip-collect",
        action="store_true",
        help="Skip data collection — re-process existing data in the database.",
    )
    parser.add_argument(
        "--skip-ml",
        action="store_true",
        help="Skip ML processing — collect and merge data only.",
    )
    args = parser.parse_args()

    if args.skip_collect and args.skip_ml:
        logger.error("Cannot use --skip-collect and --skip-ml together — nothing to do!")
        sys.exit(1)

    try:
        run_pipeline(skip_collect=args.skip_collect, skip_ml=args.skip_ml)
    except KeyboardInterrupt:
        logger.info("\nPipeline interrupted by user.")
        sys.exit(1)
    except Exception as e:
        logger.exception("Pipeline failed with error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
